import gradio as gr
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
from PIL import Image

def parse_input(array_input):
    """Converts user input string to a list of integers."""
    try:
        # Strip whitespace and convert comma-separated values to integers
        arr = [int(x.strip()) for x in array_input.split(",")]
        
        # Validate array constraints
        if len(arr) == 0:
            return False, "Error: Array cannot be empty"
        
        if len(arr) > 50:
            return False, "Error: Array too large (max 50 elements)"
        
        return True, arr
    
    except ValueError:
        return False, "Error: Please enter valid integers separated by commas (e.g., 5,2,8,1,9)"


def create_bar_chart(arr, highlight_indices=[], highlight_colors=[], title="Array Visualization"):
    """Creates a bar chart visualization of the array with color-coded highlights."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Initialize all bars with default blue color
    colors = ['skyblue'] * len(arr)
    
    # Apply highlight colors to specific indices (current element, comparing, inserted)
    for idx, color in zip(highlight_indices, highlight_colors):
        if 0 <= idx < len(arr):
            colors[idx] = color
    
    # Create bar chart
    bars = ax.bar(range(len(arr)), arr, color=colors, edgecolor='black', linewidth=1.5)
    
    # Display numeric value on top of each bar
    for i, (bar, val) in enumerate(zip(bars, arr)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Index', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(arr)))
    
    # Create color legend explaining what each color represents
    legend_elements = [
        mpatches.Patch(color='skyblue', label='Sorted portion'),
        mpatches.Patch(color='orange', label='Current element'),
        mpatches.Patch(color='red', label='Comparing/Shifting'),
        mpatches.Patch(color='lightgreen', label='Newly inserted')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    
    # Convert matplotlib plot to PIL Image for Gradio display
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    plt.close(fig)
    
    return img


def insertion_sort_with_visualization(arr):
    """
    Performs insertion sort and captures each step with visualizations.
    Returns the sorted array, text explanations, and images for each step.
    """
    steps = []
    images = []
    arr = arr.copy()  # Work on a copy to avoid modifying original
    
    # Capture initial state
    steps.append("Starting array:")
    images.append(create_bar_chart(arr, [], [], "Initial Array"))
    
    # Main insertion sort algorithm
    for i in range(1, len(arr)):
        key = arr[i]  # Current element to be inserted into sorted portion
        j = i - 1
        
        steps.append(f"\n{'='*50}")
        steps.append(f"Step {i}: Inserting element {key} (index {i})")
        steps.append(f"Sorted portion: {arr[:i]} | Unsorted: {arr[i:]}")
        
        # Show which element we're about to insert
        images.append(create_bar_chart(
            arr, 
            [i], 
            ['orange'],
            f"Step {i}: Key = {key} at index {i}"
        ))
        
        # Shift elements greater than key to the right
        shift_count = 0
        while j >= 0 and arr[j] > key:
            steps.append(f"  {arr[j]} > {key}, shifting {arr[j]} to the right")
            arr[j + 1] = arr[j]
            
            # Visualize each shift operation
            images.append(create_bar_chart(
                arr,
                [j, j+1],
                ['red', 'orange'],
                f"Step {i}: Shifting {arr[j]} right"
            ))
            
            j -= 1
            shift_count += 1
        
        # Insert key into its correct position
        arr[j + 1] = key
        steps.append(f"  Inserted {key} at position {j + 1}")
        
        # Show the array state after insertion
        images.append(create_bar_chart(
            arr,
            [j + 1],
            ['lightgreen'],
            f"Step {i}: After inserting {key}"
        ))
        
        steps.append(f"Current array: {arr}")
    
    steps.append(f"\n{'='*50}")
    steps.append(f"Sorting complete!")
    steps.append(f"Final sorted array: {arr}")
    
    # Show final sorted array with all elements highlighted in green
    images.append(create_bar_chart(
        arr,
        list(range(len(arr))),
        ['lightgreen'] * len(arr),
        "Final Sorted Array"
    ))
    
    return arr, steps, images


def visualize_insertion_sort(array_input):
    """
    Main function called by Gradio interface.
    Handles input validation and orchestrates the sorting visualization.
    """
    # Parse and validate user input
    success, result = parse_input(array_input)
    
    if not success:
        # Create error image if validation fails
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, result, ha='center', va='center', fontsize=14, color='red')
        ax.axis('off')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        error_img = Image.open(buf)
        plt.close(fig)
        return result, [error_img]
    
    # Run insertion sort with full visualization
    arr = result
    sorted_arr, steps, images = insertion_sort_with_visualization(arr)
    
    # Format step-by-step text output
    output = "\n".join(steps)
    
    # Return text explanation and ALL visualization images
    return output, images


# Configure Gradio interface with input/output components
demo = gr.Interface(
    fn=visualize_insertion_sort,
    inputs=[
        gr.Textbox(
            label="Enter array (comma-separated integers)", 
            placeholder="5,2,8,1,9",
            lines=1
        )
    ],
    outputs=[
        gr.Textbox(
            label="Step-by-Step Explanation", 
            lines=20
        ),
        gr.Gallery(
            label="Visualization Steps",
            columns=2,
            rows=2,
            height="auto"
        )
    ],
    title="Insertion Sort Visualizer",
    description="""
    **Watch how insertion sort builds a sorted array one element at a time!**
    
    Blue = Already sorted portion  
    Orange = Current element being inserted  
    Red = Elements being compared/shifted  
    Green = Newly inserted element / Final sorted array
    
    Enter numbers separated by commas (e.g., 5,2,8,1,9) and click Submit!
    Scroll through the gallery below to see each step of the sorting process.
    """,
    examples=[
        ["5,2,8,1,9"],
        ["10,7,3,15,2,8,12"],
        ["1"],
        ["5,5,5,5"],
        ["9,8,7,6,5,4,3,2,1"]
    ]
)

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()
