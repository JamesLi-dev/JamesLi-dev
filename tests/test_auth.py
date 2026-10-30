"""Authentication migration regression tests; no live credentials required."""
import os
import unittest
from base64 import b64encode
from unittest.mock import Mock, patch

import main


class TestAuthentication(unittest.TestCase):
    def fetch(self, env, status=200):
        with patch.dict(os.environ, env, clear=True):
            config = main.WakaInput()
        config.api_base_url = 'https://wakatime.com/api'
        config.time_range = 'last_30_days'
        session = Mock()
        session.get.return_value.status_code = status
        session.get.return_value.reason = 'test'
        session.get.return_value.json.return_value = {'data': {'languages': []}}
        with patch.object(main, 'wk_i', config, create=True), \
                patch.object(main.requests, 'Session') as factory:
            factory.return_value.__enter__.return_value = session
            if status in (401, 403):
                with self.assertRaises(SystemExit) as error:
                    main.fetch_stats()
                self.assertEqual(error.exception.code, 1)
            else:
                self.assertEqual(main.fetch_stats(), {'languages': []})
        session.get.assert_called_once()
        return session.get.call_args.kwargs

    def test_oauth_takes_priority_and_stays_out_of_url(self):
        args = self.fetch({'INPUT_WAKATIME_AUTH_TOKEN': ' test-token ',
                           'INPUT_WAKATIME_API_KEY': 'legacy-key'})
        self.assertEqual(args['headers'], {'Authorization': 'Bearer test-token'})
        self.assertEqual(args['url'],
                         'https://wakatime.com/api/v1/users/current/stats/last_30_days')

    def test_legacy_backend_auth_is_preserved(self):
        args = self.fetch({'INPUT_WAKATIME_API_KEY': 'legacy-key',
                           'INPUT_WAKATIME_AUTH_TOKEN': ' '})
        encoded = b64encode(b'legacy-key').decode()
        self.assertEqual(args['headers'], {'Authorization': f'Basic {encoded}'})

    def test_auth_failure_exits_without_retry(self):
        for status in (401, 403):
            with self.subTest(status=status), patch.object(main, 'sleep') as sleep:
                self.fetch({'INPUT_WAKATIME_AUTH_TOKEN': 'invalid-token'}, status)
                sleep.assert_not_called()

    def test_missing_credentials_are_reported(self):
        with patch.dict(os.environ, {}, clear=True):
            config = main.WakaInput()
        with patch.object(main.logger, 'error') as log_error:
            self.assertFalse(config.validate_input())
        self.assertIn('WAKATIME_AUTH_TOKEN', log_error.call_args.args[1])
