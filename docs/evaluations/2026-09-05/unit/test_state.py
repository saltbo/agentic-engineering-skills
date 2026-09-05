import unittest

from state import transition


class TransitionTests(unittest.TestCase):
    def test_allowed_transitions(self):
        cases = [
            ('pending', 'pay', 'paid'),
            ('pending', 'cancel', 'cancelled'),
            ('paid', 'ship', 'shipped'),
        ]
        for state, event, expected in cases:
            with self.subTest(state=state, event=event):
                self.assertEqual(transition(state, event), expected)

    def test_illegal_transitions_between_known_states_and_events(self):
        cases = [
            ('pending', 'ship'),
            ('paid', 'pay'),
            ('paid', 'cancel'),
            ('shipped', 'pay'),
            ('shipped', 'cancel'),
            ('shipped', 'ship'),
            ('cancelled', 'pay'),
            ('cancelled', 'cancel'),
            ('cancelled', 'ship'),
        ]
        for state, event in cases:
            with self.subTest(state=state, event=event):
                with self.assertRaises(ValueError):
                    transition(state, event)

    def test_invalid_state_boundaries(self):
        for state in ('', 'unknown', 'Pending', ' pending ', None):
            with self.subTest(state=state):
                with self.assertRaises(ValueError):
                    transition(state, 'pay')

    def test_invalid_event_boundaries(self):
        for state in ('pending', 'paid', 'shipped', 'cancelled'):
            for event in ('', 'unknown', 'Pay', ' pay ', None):
                with self.subTest(state=state, event=event):
                    with self.assertRaises(ValueError):
                        transition(state, event)


if __name__ == '__main__':
    unittest.main()
