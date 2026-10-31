"""Keep both README translations in sync from one statistics response."""
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import main


class TestLanguages(unittest.TestCase):
    def test_bilingual_sync_fetches_once_and_preserves_surrounding_text(self):
        template = 'Intro\n<!--START_SECTION:waka-->\nold\n<!--END_SECTION:waka-->\nFooter'
        stats = {'start': '2026-10-01T00:00:00Z', 'end': '2026-10-30T00:00:00Z'}
        for category in ('languages', 'editors', 'categories', 'operating_systems'):
            stats[category] = [{'name': 'Example', 'text': '1 hr', 'percent': 100}]
        config = SimpleNamespace(gh_token='test', repository='test/profile',
                                 commit_message='Update stats', show_title=True,
                                 show_total_time=False, show_time=True, block_style='░▒▓█')
        repo = Mock()
        repo.get_readme.return_value = SimpleNamespace(
            path='README.md', decoded_content=template.encode(), sha='en-sha')
        repo.get_contents.return_value = SimpleNamespace(
            path='README.zh-CN.md', decoded_content=template.encode(), sha='zh-sha')
        with patch.object(main, 'wk_i', config, create=True), \
                patch.object(main, 'wk_c', main.WakaConstants(), create=True), \
                patch.object(main, 'Github') as github, \
                patch.object(main, 'fetch_stats', return_value=stats) as fetch:
            github.return_value.get_repo.return_value = repo
            main.genesis()
        fetch.assert_called_once()
        self.assertEqual(repo.update_file.call_count, 2)
        repo.get_contents.assert_called_once_with('README.zh-CN.md')
        self.assertEqual([call.kwargs['path'] for call in repo.update_file.call_args_list],
                         ['README.md', 'README.zh-CN.md'])
        en, zh = [call.kwargs['content'] for call in repo.update_file.call_args_list]
        self.assertIn('使用代码『 语言 』', zh)
        self.assertNotIn('到:', zh)
        for label in ('Languages', 'Editors', 'Activities', 'Operating Systems'):
            self.assertIn(f'{label}: 2026-10-01 - 2026-10-30', en)
        self.assertNotRegex(en, r'[\u4e00-\u9fff]')
        for content in (zh, en):
            self.assertTrue(content.startswith('Intro\n'))
            self.assertTrue(content.endswith('\nFooter'))
            self.assertEqual(content.count('Example'), 4)
