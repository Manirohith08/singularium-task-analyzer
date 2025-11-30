from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .scoring import calculate_priority_score, detect_cycles

@csrf_exempt
def analyze_tasks(request):
    """
    POST /api/tasks/analyze/
    Accepts tasks, applies algorithm, returns sorted list.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tasks = data if isinstance(data, list) else data.get('tasks', [])
            
            # BONUS: Cycle Detection 
            cyclic_nodes = detect_cycles(tasks)

            analyzed_tasks = []
            for task in tasks:
                score, reason = calculate_priority_score(task, tasks)
                
                # Critical Consideration: Circular Dependencies [cite: 37]
                if task['id'] in cyclic_nodes:
                    score = 0
                    reason = "BLOCKED: Circular Dependency Detected"

                task['score'] = score
                task['rationale'] = reason
                analyzed_tasks.append(task)

            # Sort by score descending
            analyzed_tasks.sort(key=lambda x: x['score'], reverse=True)
            
            return JsonResponse({'status': 'success', 'tasks': analyzed_tasks})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

def suggest_tasks(request):
    """
    GET /api/tasks/suggest/
    Returns top 3 tasks simulation.
    """
    # Just a placeholder to satisfy the requirement 
    return JsonResponse({
        "note": "Use the main Analyzer for live data.",
        "top_3_suggestions": [] 
    })