import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from newsintel.pipeline import canonical, feed_items, validate, collect, main, connect, history

ROOT = Path(__file__).resolve().parent.parent

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.edition = json.loads((ROOT / 'editorial.example.json').read_text())
        self.edition['jobs'] = []
        self.packet = {'collected_at': datetime.now(timezone.utc).isoformat(), 'news': [], 'jobs': [], 'errors': []}

    def test_malformed_editorial_rejected(self):
        self.assertTrue(validate([], self.packet, []))
        self.edition["jobs"] = "bad"
        self.assertTrue(validate(self.edition, self.packet, []))

    def test_valid_structure(self):
        self.assertEqual(validate(self.edition, self.packet, []), [])

    def test_tracking_and_fragment_removed(self):
        self.assertEqual(canonical('https://EXAMPLE.com/story?utm_source=test&id=3#top'), 'https://example.com/story?id=3')

    def test_feed_recency_and_atom(self):
        now = datetime(2026, 10, 23, tzinfo=timezone.utc)
        raw = b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>New</title><link href="https://example.com/new"/><published>2026-10-22T12:00:00Z</published></entry><entry><title>Old</title><link href="https://example.com/old"/><published>2020-01-01T00:00:00Z</published></entry></feed>'
        self.assertEqual([r['title'] for r in feed_items(raw, now, 72)], ['New'])

    def test_duplicate_and_repeated_events(self):
        e = copy.deepcopy(self.edition)
        e['developments'][1]['event_id'] = e['developments'][0]['event_id']
        self.assertTrue(any('Duplicate' in x for x in validate(e, self.packet, [])))
        self.assertTrue(any('Repeated' in x for x in validate(self.edition, self.packet, [self.edition])))

    def test_fabricated_job_rejected(self):
        self.edition['jobs'] = [{'id': 'invented'}]
        self.assertTrue(any('collected' in x for x in validate(self.edition, self.packet, [])))

    def test_hyphens_and_missing_sources_rejected(self):
        self.edition['linkedin_post'] = 'Not-ready — yet'
        self.edition['developments'][0]['sources'] = []
        errors = validate(self.edition, self.packet, [])
        self.assertTrue(any('punctuation' in x for x in errors))
        self.assertTrue(any('sources' in x for x in errors))

    def test_source_failure_recorded(self):
        with patch('newsintel.pipeline.fetch', side_effect=OSError('offline')):
            packet = collect({'feeds':['https://example.com/feed'], 'greenhouse_boards':[]}, datetime.now(timezone.utc))
        self.assertEqual(len(packet['errors']), 1)
        self.assertEqual(packet['news'], [])

    def test_end_to_end_draft_review_and_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            packet, editorial = root/'packet.json', root/'input.json'
            packet.write_text(json.dumps(self.packet))
            editorial.write_text(json.dumps(self.edition))
            args = ['--packet',str(packet),'--editorial',str(editorial),'--state',str(root/'history.sqlite'),'--output',str(root/'out')]
            self.assertEqual(main(['run']+args), 0)
            self.assertEqual(history(connect(root/'history.sqlite')), [])
            self.assertEqual(main(['finalize']+args), 1)
            self.edition['review'] = {'approved':True,'reviewer':'Test reviewer'}
            editorial.write_text(json.dumps(self.edition))
            self.assertEqual(main(['finalize']+args), 0)
            self.assertEqual(len(history(connect(root/'history.sqlite'))), 1)
            self.assertEqual(len(list((root/'out').glob('*/briefing.md'))), 1)

if __name__ == '__main__':
    unittest.main()
