def insertion_sort(arr):
    """
    Performs insertion sort and returns the sorted array with step-by-step details.
    """
    steps = []
    arr = arr.copy()  # Don't modify the original
    
    steps.append(f"Starting array: {arr}")
    
    # Start from second element (index 1)
    for i in range(1, len(arr)):
        key = arr[i]  # Element to be inserted
        j = i - 1
        
        steps.append(f"\n--- Step {i} ---")
        steps.append(f"Current element to insert: {key} at position {i}")
        steps.append(f"Comparing with sorted portion: {arr[:i]}")
        
        # Move elements greater than key one position ahead
        comparisons = 0
        while j >= 0 and arr[j] > key:
            steps.append(f"  {arr[j]} > {key}, shift {arr[j]} right")
            arr[j + 1] = arr[j]
            j -= 1
            comparisons += 1
        
        # Insert the key at correct position
        arr[j + 1] = key
        steps.append(f"Insert {key} at position {j + 1}")
        steps.append(f"Array after insertion: {arr}")
    
    steps.append(f"\n✓ Final sorted array: {arr}")
    return arr, steps


# Test it
if __name__ == "__main__":
    test_array = [5, 2, 8, 1, 9]
    sorted_arr, steps = insertion_sort(test_array)
    
    print("\n".join(steps))
