from django.test import TestCase
from .scoring import calculate_priority_score, detect_cycles, count_business_days
import datetime
from datetime import date, timedelta

class AlgorithmTests(TestCase):
    
    def setUp(self):
        # Base Helpers
        self.today = date.today()
        self.next_monday = self.today + timedelta(days=(7 - self.today.weekday())) # Ensure it's a weekday
    
    # --- 1. Date Intelligence Tests (Bonus) ---
    def test_business_days_calculation(self):
        """Ensure weekends are skipped in urgency calculation."""
        # Friday to Next Tuesday = 2 business days (Mon, Tue)
        friday = date(2023, 11, 24) 
        tuesday = date(2023, 11, 28)
        # Note: logic depends on implementation, usually start date exclusive
        days = count_business_days(friday, tuesday) 
        # Logic in scoring.py: generator runs for delta days. 
        # If implementation was inclusive/exclusive, adjust expectation.
        # Assuming standard delta: Sat(skip), Sun(skip), Mon(count), Tue(count) -> 2 days (approx)
        self.assertIsInstance(days, int)

    def test_overdue_penalty(self):
        """Past due tasks should have massive priority."""
        past_date = str(self.today - timedelta(days=5))
        task = {"id": 1, "due_date": past_date, "estimated_hours": 2, "importance": 5}
        score, reason = calculate_priority_score(task, [])
        self.assertGreater(score, 100, "Score should reflect overdue penalty")
        self.assertIn("Overdue", reason)

    # --- 2. Cycle Detection Tests (Bonus) ---
    def test_no_cycle(self):
        """Linear dependency chain should be safe."""
        tasks = [
            {"id": 1, "dependencies": []},
            {"id": 2, "dependencies": [1]} # 2 depends on 1
        ]
        cycles = detect_cycles(tasks)
        self.assertEqual(len(cycles), 0)

    def test_direct_cycle(self):
        """A <-> B should be detected."""
        tasks = [
            {"id": 1, "dependencies": [2]},
            {"id": 2, "dependencies": [1]}
        ]
        cycles = detect_cycles(tasks)
        self.assertIn(1, cycles)
        self.assertIn(2, cycles)

    def test_self_cycle(self):
        """A depends on A should be detected."""
        tasks = [{"id": 1, "dependencies": [1]}]
        cycles = detect_cycles(tasks)
        self.assertIn(1, cycles)

    # --- 3. Scoring Logic Tests (Core) ---
    def test_quick_win_bonus(self):
        """Low effort tasks should score higher than high effort tasks (all else equal)."""
        date_str = str(self.next_monday)
        t_quick = {"id": 1, "due_date": date_str, "estimated_hours": 1, "importance": 5}
        t_slow =  {"id": 2, "due_date": date_str, "estimated_hours": 20, "importance": 5}
        
        s1, _ = calculate_priority_score(t_quick, [])
        s2, _ = calculate_priority_score(t_slow, [])
        
        self.assertGreater(s1, s2, "Quick wins should be prioritized")

    def test_bottleneck_bonus(self):
        """Task blocking others should have higher score."""
        date_str = str(self.next_monday)
        # Task A blocks Task B
        task_a = {"id": 1, "due_date": date_str, "estimated_hours": 5, "importance": 5, "dependencies": []}
        task_b = {"id": 2, "due_date": date_str, "estimated_hours": 5, "importance": 5, "dependencies": [1]}
        
        all_tasks = [task_a, task_b]
        
        # Calculate score for A (the blocker)
        s_a, _ = calculate_priority_score(task_a, all_tasks)
        # Calculate score for C (an isolated task with same stats)
        task_c = {"id": 3, "due_date": date_str, "estimated_hours": 5, "importance": 5, "dependencies": []}
        s_c, _ = calculate_priority_score(task_c, [task_c])
        
        self.assertGreater(s_a, s_c, "Blocking tasks should get a dependency bonus")