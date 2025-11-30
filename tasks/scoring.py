import datetime
from datetime import date

def count_business_days(start_date, end_date):
    """
    BONUS: Date Intelligence.
    Calculates urgency excluding weekends.
    """
    if start_date > end_date:
        return 0
    day_generator = (start_date + datetime.timedelta(x + 1) for x in range((end_date - start_date).days))
    return sum(1 for day in day_generator if day.weekday() < 5)

def detect_cycles(tasks):
    """
    BONUS: Dependency Graph Visualization logic.
    Returns a set of task IDs involved in circular dependencies.
    """
    adj = {t['id']: t.get('dependencies', []) for t in tasks}
    visited = set()
    recursion_stack = set()
    cycles = set()

    def dfs(node):
        visited.add(node)
        recursion_stack.add(node)
        
        for neighbor in adj.get(node, []):
            # Handle case where dependency ID exists in list but not in task input
            if neighbor not in adj: 
                continue
                
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in recursion_stack:
                cycles.add(node)
                return True
        
        recursion_stack.remove(node)
        return False

    for task in tasks:
        if task['id'] not in visited:
            dfs(task['id'])
    
    return cycles

def calculate_priority_score(task, all_tasks):
    """
    Core Algorithm[cite: 27].
    Weighs Urgency, Importance, Effort, and Dependencies.
    """
    today = date.today()
    try:
        due_date = datetime.datetime.strptime(task['due_date'], "%Y-%m-%d").date()
    except ValueError:
        return 0, "Invalid Date Format"

    # 1. Urgency Score (Weighted High)
    days_until_due = count_business_days(today, due_date)
    
    if due_date < today:
        # Past due tasks get massive priority [cite: 29]
        urgency_score = 100 + (abs((due_date - today).days) * 10)
        urgency_note = "Overdue"
    elif days_until_due == 0:
        urgency_score = 95
        urgency_note = "Due Today"
    else:
        # Exponential decay
        urgency_score = 100 / (days_until_due + 1)
        urgency_note = f"{days_until_due} days left"

    # 2. Importance Score (Normalized 1-10 to 1-100) [cite: 30]
    importance_score = task['importance'] * 10

    # 3. Effort Score (Quick Wins) [cite: 31]
    # Invert hours: Lower hours = Higher score
    effort_score = max(0, 50 - (task['estimated_hours'] * 2))

    # 4. Dependency Score [cite: 31]
    # If this task blocks others, it ranks higher
    blocked_tasks_count = sum(1 for t in all_tasks if task['id'] in t.get('dependencies', []))
    dependency_score = blocked_tasks_count * 20

    # Final Calculation: Weighted Average
    # Urgency (35%), Importance (30%), Dependencies (25%), Effort (10%)
    final_score = (
        (urgency_score * 0.35) + 
        (importance_score * 0.30) + 
        (dependency_score * 0.25) + 
        (effort_score * 0.10)
    )

    # Build Explanation 
    reasons = [urgency_note]
    if task['importance'] >= 8: reasons.append("High Importance")
    if blocked_tasks_count > 0: reasons.append(f"Blocks {blocked_tasks_count} tasks")
    if task['estimated_hours'] <= 2: reasons.append("Quick Win")

    return round(final_score, 1), ", ".join(reasons)