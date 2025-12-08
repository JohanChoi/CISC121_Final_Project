import gradio as gr

def parse_input(array_input):
    """Converts user input string to a list of integers."""
    try:
        arr = [int(x.strip()) for x in array_input.split(",")]
        
        if len(arr) == 0:
            return False, "Error: Array cannot be empty"
        
        if len(arr) > 50:
            return False, "Error: Array too large (max 50 elements)"
        
        return True, arr
    
    except ValueError:
        return False, "Error: Please enter valid integers separated by commas (e.g., 5,2,8,1,9)"


def insertion_sort(arr):
    """Performs insertion sort and returns steps."""
    steps = []
    arr = arr.copy()
    
    steps.append(f"Starting array: {arr}")
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        steps.append(f"\n--- Step {i} ---")
        steps.append(f"Current element to insert: {key} at position {i}")
        steps.append(f"Comparing with sorted portion: {arr[:i]}")
        
        while j >= 0 and arr[j] > key:
            steps.append(f"  {arr[j]} > {key}, shift {arr[j]} right")
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
        steps.append(f"Insert {key} at position {j + 1}")
        steps.append(f"Array after insertion: {arr}")
    
    steps.append(f"\n✓ Final sorted array: {arr}")
    return arr, steps


def visualize_insertion_sort(array_input):
    """Main function called by Gradio interface."""
    # Parse and validate input
    success, result = parse_input(array_input)
    
    if not success:
        return result  # Return error message
    
    # Run insertion sort
    arr = result
    sorted_arr, steps = insertion_sort(arr)
    
    # Format output nicely
    output = "\n".join(steps)
    return output


# Create Gradio interface
demo = gr.Interface(
    fn=visualize_insertion_sort,
    inputs=[
        gr.Textbox(
            label="Enter array (comma-separated integers)", 
            placeholder="5,2,8,1,9",
            lines=1
        )
    ],
    outputs=gr.Textbox(
        label="Insertion Sort Steps", 
        lines=20
    ),
    title="🔢 Insertion Sort Visualizer",
    description="Watch how insertion sort builds a sorted array one element at a time!",
    examples=[
        ["5,2,8,1,9"],
        ["10,7,3,15,2,8,12"],
        ["1"],
        ["5,5,5,5"],
        ["9,8,7,6,5,4,3,2,1"]
    ]
)

if __name__ == "__main__":
    demo.launch()
