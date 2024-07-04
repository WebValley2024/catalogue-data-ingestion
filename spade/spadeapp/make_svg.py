import matplotlib.pyplot as plt
import numpy as np
import io

def clean_data(xarr, yarr, sources):
    return zip(*[(float(x), float(y), s) for x, y, s in zip(xarr, yarr, sources) if isinstance(x, float) or x != "" or "-" not in x])

def get_svg(xarr, yarr, sources):
    xarr, yarr, s_clean = clean_data(xarr, yarr, sources)
    
    # Create a figure with specified size
    plt.figure(figsize=(10, 6))  # Adjust the size as needed
    #plt.style.use('seaborn-v0_8-white')
    print(plt.style.available)
    plt.subplot(111, projection='aitoff')
    plt.grid(True)
    
    # Define marker and color for each source
    markers_list = ('o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_')
    colors_list = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
    
    markers = {source: markers_list[i % len(markers_list)] for i, source in enumerate(set(s_clean))}
    colors = {source: colors_list[i % len(colors_list)] for i, source in enumerate(set(s_clean))}
    
    # Plot each point with the corresponding marker and color
    for x, y, s in zip(xarr, yarr, s_clean):
        plt.scatter(x, y, marker=markers[s], color=colors[s], label=s)
    
    # Create a legend to avoid duplicate labels
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right', bbox_to_anchor=(1.2, 1))
    
    # Save the plot to a BytesIO object
    svg_buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(svg_buffer, format='svg')
    svg_buffer.seek(0)
    
    # Return the SVG content
    return f"<div>{svg_buffer.getvalue().decode('utf-8')}</div>"

# Get the SVG content
#get_svg(xarr, yarr, s_clean)