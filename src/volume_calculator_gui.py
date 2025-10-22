import sys
import os

# Set matplotlib backend first
import matplotlib
matplotlib.use('TkAgg')

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import sympy as sp
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog, filedialog
    
    # Optional STL support
    try:
        from stl import mesh
        STL_AVAILABLE = True
        print("STL support: Enabled")
    except ImportError:
        STL_AVAILABLE = False
        print("STL support: Disabled")
        
    print("✅ All imports successful!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class VolumeCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Volume of Revolution Calculator")
        self.root.geometry("900x700")
        self.cross_section_var = tk.BooleanVar(value=False)
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Volume of Revolution Calculator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Function inputs
        ttk.Label(main_frame, text="Enter Functions (use 'x' as variable):", 
                 font=("Arial", 10, "bold")).grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=5)
        
        self.func1 = ttk.Entry(main_frame, width=30)
        self.func1.insert(0, "x**2")
        self.func1.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        ttk.Label(main_frame, text="f₁(x)").grid(row=2, column=3, padx=5)
        
        self.func2 = ttk.Entry(main_frame, width=30)
        self.func2.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        ttk.Label(main_frame, text="f₂(x) (optional)").grid(row=3, column=3, padx=5)
        
        self.func3 = ttk.Entry(main_frame, width=30)
        self.func3.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        ttk.Label(main_frame, text="f₃(x) (optional)").grid(row=4, column=3, padx=5)
        
        # Revolution parameters
        ttk.Label(main_frame, text="Revolution Parameters:", 
                 font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=4, sticky=tk.W, pady=10)
        
        ttk.Label(main_frame, text="Revolve Around:").grid(row=6, column=0, sticky=tk.W)
        self.axis_var = tk.StringVar(value="x")
        ttk.Combobox(main_frame, textvariable=self.axis_var, 
                    values=["x", "y"], state="readonly", width=10).grid(row=6, column=1, sticky=tk.W)
        
        ttk.Label(main_frame, text="Revolve Function:").grid(row=7, column=0, sticky=tk.W)
        self.func_var = tk.StringVar(value="f₁(x)")
        ttk.Combobox(main_frame, textvariable=self.func_var, 
                    values=["f₁(x)", "f₂(x)", "f₃(x)"], state="readonly", width=10).grid(row=7, column=1, sticky=tk.W)
        
        ttk.Label(main_frame, text="Method:").grid(row=8, column=0, sticky=tk.W)
        self.method_var = tk.StringVar(value="washer")
        ttk.Combobox(main_frame, textvariable=self.method_var, 
                    values=["disk", "washer"], state="readonly", width=10).grid(row=8, column=1, sticky=tk.W)
        
        # Cross-section option
        ttk.Checkbutton(main_frame, text="Show Cross-Sections", 
                       variable=self.cross_section_var).grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Limits
        ttk.Label(main_frame, text="Integration Limits:", 
                 font=("Arial", 10, "bold")).grid(row=10, column=0, columnspan=4, sticky=tk.W, pady=10)
        
        ttk.Label(main_frame, text="Lower limit a:").grid(row=11, column=0, sticky=tk.W)
        self.a_var = tk.StringVar(value="0")
        ttk.Entry(main_frame, textvariable=self.a_var, width=10).grid(row=11, column=1, sticky=tk.W)
        
        ttk.Label(main_frame, text="Upper limit b:").grid(row=12, column=0, sticky=tk.W)
        self.b_var = tk.StringVar(value="2")
        ttk.Entry(main_frame, textvariable=self.b_var, width=10).grid(row=12, column=1, sticky=tk.W)
        
        ttk.Label(main_frame, text="Δx step:").grid(row=13, column=0, sticky=tk.W)
        self.dx_var = tk.StringVar(value="0.01")
        ttk.Entry(main_frame, textvariable=self.dx_var, width=10).grid(row=13, column=1, sticky=tk.W)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=14, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="Generate Visualization", 
                  command=self.calculate_and_plot).grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text="Export to STL", 
                  command=self.export_to_stl).grid(row=0, column=1, padx=5)
        
        ttk.Button(button_frame, text="Send to 3D Printer", 
                  command=self.send_to_printer).grid(row=0, column=2, padx=5)
        
        # Results text area
        ttk.Label(main_frame, text="Results:", 
                 font=("Arial", 10, "bold")).grid(row=15, column=0, sticky=tk.W, pady=5)
        
        self.results_text = tk.Text(main_frame, height=10, width=80)
        self.results_text.grid(row=16, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=17, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def parse_functions(self):
        """Parse the function strings into callable functions"""
        funcs = []
        func_strs = [self.func1.get(), self.func2.get(), self.func3.get()]
        
        for func_str in func_strs:
            if func_str.strip():
                try:
                    func = eval(f"lambda x: {func_str}")
                    # Test the function
                    test_val = func(1.0)
                    funcs.append(func)
                except Exception as e:
                    messagebox.showerror("Error", f"Invalid function: {func_str}\nError: {e}")
                    return None
        return funcs if funcs else None
    
    def calculate_volume(self, funcs, revolve_index, a, b, dx):
        """Calculate volume using numerical integration"""
        volume = 0
        x_vals = np.arange(a, b, dx)
        
        if self.axis_var.get() == 'x':
            # Revolution around x-axis
            for x in x_vals:
                if self.method_var.get() == 'disk':
                    radius = funcs[revolve_index](x)
                    volume += np.pi * (radius ** 2) * dx
                else:  # washer method
                    outer_radius = funcs[revolve_index](x)
                    inner_radius_sq = 0
                    for i, func in enumerate(funcs):
                        if i != revolve_index:
                            inner_radius_sq += (func(x) ** 2)
                    volume += np.pi * ((outer_radius ** 2) - inner_radius_sq) * dx
        else:
            # Revolution around y-axis (shell method)
            for x in x_vals:
                radius = x
                height = funcs[revolve_index](x)
                if self.method_var.get() == 'washer' and len(funcs) > 1:
                    for i, func in enumerate(funcs):
                        if i != revolve_index:
                            height -= func(x)
                volume += 2 * np.pi * radius * abs(height) * dx
                
        return volume
    
    def calculate_and_plot(self):
        """Main calculation and plotting function"""
        try:
            # Parse inputs
            funcs = self.parse_functions()
            if not funcs:
                return
                
            a = float(self.a_var.get())
            b = float(self.b_var.get())
            dx = float(self.dx_var.get())
            
            revolve_index = {"f₁(x)": 0, "f₂(x)": 1, "f₃(x)": 2}[self.func_var.get()]
            if revolve_index >= len(funcs):
                messagebox.showerror("Error", "Selected function is not defined")
                return
            
            # Calculate volume
            volume = self.calculate_volume(funcs, revolve_index, a, b, dx)
            
            # Create visualization
            self.create_plots(funcs, revolve_index, a, b, volume)
            
            # Display results
            self.display_results(funcs, revolve_index, a, b, dx, volume)
            
            self.status_var.set("Visualization generated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {e}")
            self.status_var.set(f"Error: {e}")
    
    def create_plots(self, funcs, revolve_index, a, b, volume):
        """Create 2D and 3D plots with optional cross-sections"""
        fig = plt.figure(figsize=(15, 6))
        
        # 3D Plot
        ax1 = fig.add_subplot(121, projection='3d')
        
        x = np.linspace(a, b, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        X, T = np.meshgrid(x, theta)
        
        if self.axis_var.get() == 'x':
            revolve_func = funcs[revolve_index]
            R_outer = revolve_func(X)
            Y_outer = R_outer * np.cos(T)
            Z_outer = R_outer * np.sin(T)
            
            ax1.plot_surface(X, Y_outer, Z_outer, alpha=0.7, color='blue')
            
            if self.method_var.get() == 'washer':
                for i, func in enumerate(funcs):
                    if i != revolve_index:
                        R_inner = func(X)
                        Y_inner = R_inner * np.cos(T)
                        Z_inner = R_inner * np.sin(T)
                        ax1.plot_surface(X, Y_inner, Z_inner, alpha=0.5, color='red')
            
            # Add cross-sections if enabled
            if self.cross_section_var.get():
                # Add cross-sections at specific theta values
                for theta_val in [0, np.pi/2, np.pi, 3*np.pi/2]:
                    x_cross = np.linspace(a, b, 30)
                    y_cross = revolve_func(x_cross) * np.cos(theta_val)
                    z_cross = revolve_func(x_cross) * np.sin(theta_val)
                    ax1.plot(x_cross, y_cross, z_cross, 'k-', linewidth=2, alpha=0.8)
            
            ax1.set_title(f'3D Revolution around X-axis\n({self.method_var.get().title()} Method)')
        else:
            revolve_func = funcs[revolve_index]
            for x_val in np.linspace(a, b, 20):
                radius = revolve_func(x_val)
                theta_circle = np.linspace(0, 2*np.pi, 30)
                x_circle = radius * np.cos(theta_circle)
                z_circle = radius * np.sin(theta_circle)
                y_circle = np.full_like(x_circle, x_val)
                ax1.plot(x_circle, y_circle, z_circle, 'b-', alpha=0.6)
            
            # Add cross-sections if enabled
            if self.cross_section_var.get():
                # Add cross-sections at specific x values
                for x_val in np.linspace(a, b, 5):
                    radius = revolve_func(x_val)
                    theta_circle = np.linspace(0, 2*np.pi, 30)
                    x_circle = radius * np.cos(theta_circle)
                    z_circle = radius * np.sin(theta_circle)
                    y_circle = np.full_like(x_circle, x_val)
                    ax1.plot(x_circle, y_circle, z_circle, 'k-', linewidth=2, alpha=0.8)
            
            ax1.set_title(f'3D Revolution around Y-axis\n(Shell Method)')
        
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        
        # 2D Plot
        ax2 = fig.add_subplot(122)
        x_vals = np.linspace(a, b, 200)
        
        colors = ['blue', 'red', 'green']
        labels = ['f₁(x)', 'f₂(x)', 'f₃(x)']
        
        for i, func in enumerate(funcs):
            y_vals = func(x_vals)
            ax2.plot(x_vals, y_vals, color=colors[i], linewidth=2, label=labels[i])
            if i == revolve_index:
                ax2.fill_between(x_vals, y_vals, alpha=0.3, color=colors[i])
        
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_title('2D Area Between Curves')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def generate_stl_mesh(self, funcs, revolve_index, a, b, num_points=50):
        """Generate a 3D mesh for STL export"""
        if not STL_AVAILABLE:
            messagebox.showerror("Error", "numpy-stl library not available. Please install it with: pip install numpy-stl")
            return None
            
        try:
            revolve_func = funcs[revolve_index]
            
            # Create vertices for the revolution
            u = np.linspace(a, b, num_points)  # x values
            v = np.linspace(0, 2*np.pi, num_points)  # theta values
            
            vertices = []
            
            if self.axis_var.get() == 'x':
                # Revolution around x-axis
                for x_val in u:
                    radius = revolve_func(x_val)
                    for theta in v:
                        y_val = radius * np.cos(theta)
                        z_val = radius * np.sin(theta)
                        vertices.append([x_val, y_val, z_val])
            else:
                # Revolution around y-axis
                for y_val in u:
                    radius = revolve_func(y_val)
                    for theta in v:
                        x_val = radius * np.cos(theta)
                        z_val = radius * np.sin(theta)
                        vertices.append([x_val, y_val, z_val])
            
            vertices = np.array(vertices)
            
            # Create faces (simplified triangulation)
            # This is a simplified approach - for production use, consider a proper triangulation
            faces = []
            for i in range(num_points-1):
                for j in range(num_points-1):
                    # Create two triangles for each quad
                    v1 = i * num_points + j
                    v2 = i * num_points + j + 1
                    v3 = (i + 1) * num_points + j
                    v4 = (i + 1) * num_points + j + 1
                    
                    faces.append([v1, v2, v3])
                    faces.append([v2, v4, v3])
            
            # Create the mesh
            stl_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
            for i, face in enumerate(faces):
                for j in range(3):
                    stl_mesh.vectors[i][j] = vertices[face[j]]
            
            return stl_mesh
            
        except Exception as e:
            messagebox.showerror("Error", f"STL generation error: {e}")
            return None
    
    def export_to_stl(self):
        """Export the 3D model to STL file"""
        try:
            # Parse inputs
            funcs = self.parse_functions()
            if not funcs:
                return
                
            a = float(self.a_var.get())
            b = float(self.b_var.get())
            
            revolve_index = {"f₁(x)": 0, "f₂(x)": 1, "f₃(x)": 2}[self.func_var.get()]
            if revolve_index >= len(funcs):
                messagebox.showerror("Error", "Selected function is not defined")
                return
            
            # Generate STL mesh
            stl_mesh = self.generate_stl_mesh(funcs, revolve_index, a, b)
            if stl_mesh is None:
                return
            
            # Ask for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".stl",
                filetypes=[("STL files", "*.stl"), ("All files", "*.*")],
                title="Save STL file as"
            )
            
            if filename:
                stl_mesh.save(filename)
                self.status_var.set(f"STL file saved successfully: {filename}")
                messagebox.showinfo("Success", f"STL file saved successfully:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Export error: {e}")
            self.status_var.set(f"Export error: {e}")
    
    def send_to_printer(self):
        """Simulate sending to 3D printer (in a real application, this would interface with printer software)"""
        try:
            # For demonstration, we'll just export to STL and show a message
            self.export_to_stl()
            
            # In a real implementation, you would:
            # 1. Export to STL
            # 2. Send to printer software via API
            # 3. Show printer status/dialog
            
            messagebox.showinfo("3D Printing", 
                              "In a full implementation, this would send the model to your 3D printer.\n\n"
                              "For now, the STL file has been saved and can be manually loaded into your slicer software.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Print error: {e}")
    
    def display_results(self, funcs, revolve_index, a, b, dx, volume):
        """Display results in the text area"""
        func_strs = [self.func1.get(), self.func2.get(), self.func3.get()]
        
        results = "=" * 60 + "\n"
        results += "VOLUME OF REVOLUTION - RESULTS\n"
        results += "=" * 60 + "\n\n"
        results += "FUNCTIONS:\n"
        
        for i, func_str in enumerate(func_strs):
            if func_str.strip():
                revolve_ind = " ⭐ (REVOLVE)" if i == revolve_index else ""
                results += f"  f{i+1}(x) = {func_str}{revolve_ind}\n"
        
        results += f"\nPARAMETERS:\n"
        results += f"  Axis of revolution: {self.axis_var.get().upper()}-axis\n"
        results += f"  Lower limit (a): {a}\n"
        results += f"  Upper limit (b): {b}\n"
        results += f"  Method: {self.method_var.get().title()}\n"
        results += f"  Δx step size: {dx}\n"
        results += f"  Show cross-sections: {'Yes' if self.cross_section_var.get() else 'No'}\n"
        
        results += f"\nRESULTS:\n"
        results += f"  Calculated Volume: {volume:.6f} cubic units\n"
        
        # Add STL export info
        if STL_AVAILABLE:
            results += f"\nEXPORT:\n"
            results += f"  3D model can be exported as STL for 3D printing\n"
        else:
            results += f"\nNOTE:\n"
            results += f"  Install numpy-stl for 3D export: pip install numpy-stl\n"
            
        results += "=" * 60
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, results)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    # Check if required packages are installed
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        import sympy as sp
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install required packages:")
        print("pip install numpy matplotlib sympy")
        sys.exit(1)
    
    # Check for STL support
    if not STL_AVAILABLE:
        print("Note: numpy-stl not installed. 3D export will not be available.")
        print("Install with: pip install numpy-stl")
    
    app = VolumeCalculator()
    app.run()
