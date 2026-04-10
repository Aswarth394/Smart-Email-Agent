# bfs_thread.py
from collections import deque

def analyze_thread_bfs(start_email_id, thread_map, max_nodes=3):
    """
    Traverses an email thread using Bounded BFS.
    Limits the search to the most relevant 'max_nodes' to optimize performance.
    """
    visited = set()
    queue = deque([start_email_id])
    full_thread_context = [] 

    print(f"--- Starting Bounded BFS (Limit: {max_nodes}) ---")

    while queue and len(full_thread_context) < max_nodes:
        current_id = queue.popleft()
        
        if current_id not in visited:
            visited.add(current_id)
            full_thread_context.append(current_id)
            
            # thread_map logic: finds child nodes (replies)
            replies = thread_map.get(current_id, [])
            for reply_id in replies:
                if reply_id not in visited:
                    queue.append(reply_id)

    return full_thread_context

# --- TEST TRIGGER: This will now show output in your terminal ---
if __name__ == "__main__":
    # Mock data: A thread with 12 emails to test the '3 email' limit
    mock_thread = {
        'Root': ['R1', 'R2'],
        'R1': ['R1_a', 'R1_b', 'R1_c'],
        'R2': ['R2_a', 'R2_b'],
        'R1_a': ['End1', 'End2'],
        'R1_b': ['End3', 'End4'], # This will exceed the 3 limit
    }
    
    print("[🔴 STAGING TASK] Testing Bounded BFS...")
    result = analyze_thread_bfs('Root', mock_thread, max_nodes=3)
    
    print(f"\nFinal Traversal Order (Limited to 3):")
    print(result)
    print(f"Total Emails Found: {len(result)}")