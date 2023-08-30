from pathlib import Path as Path_X
from manim import *
import matplotlib.cm
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


manim_path = Path_X("C:/Users/Bowen/PycharmProjects/Entropy_Game/Code/Manim")
version_3_path = manim_path.parent / "Version_3"

class setup:
    def __init__(self):
        grids_npy_path = version_3_path / 'grids.npy'
        density_states_path = version_3_path / 'density_of_states.npy'
        entrop_path = version_3_path / 'entropies.npy'

        self.grid = np.load(grids_npy_path)
        self.density_states = np.load(density_states_path)
        self.entropies = np.load(entrop_path)
        self.relative_entrop = self.entropies - self.entropies[0]
        self.iterations = self.grid.shape[0]


    def convert_rgb(self, grid_data : np.array, cmap : str):
        """
        To prepare for the Image Mobject in Manim, we will need to convert it to an RGB image
        From the Grid data that was provided
        """
        max_value = np.max(grid_data)
        min_value = np.min(grid_data)
        self.cmap = matplotlib.colormaps.get_cmap(cmap)
        self.normalize = plt.Normalize(min_value, max_value)
        self.grid_data_RGB = self.cmap(self.normalize(grid_data))
        return (self.grid_data_RGB[:, :, :3] * 255).astype(np.uint8)

    def get_rgb_values(self, the_Grid ,colormap : str):
        """
        This function is meant to convert all the Grids into false color coding by calling the
        convert_rgb function defined before for 400 iterations for a valid colormap from matplotlib
        """
        RGB=np.array([self.convert_rgb(the_Grid[i, :, :],cmap=plt.get_cmap(colormap)) for i in range(self.iterations)])
        return RGB

    def entropy_setup(self):
        """
        A simple attribute to prepare for the entropy
        """
        start = 0
        stop = (self.grid.shape[0] - 1) * 4
        step = 4
        entropy = np.array(self.entropies)
        x_index = np.arange(start, stop + step, step)

        return start, stop, x_index, entropy

class PreChecks:
    def __init__(self):
        self.Setup = setup()
        self.loaded_grid = self.Setup.grid
        self.loaded_states = self.Setup.density_states
        self.Entropy_list = self.Setup.entropies
        self.relative_entropy = self.Entropy_list - self.Entropy_list[0]
        self.grid_data = self.Setup.get_rgb_values(self.loaded_grid, 'plasma')     # --> This should also be a 4 dim array
        self.entropy_states = self.Setup.get_rgb_values(self.loaded_states, 'viridis')  # --> This should be a 4 dim array

    def animation_loop(self, animate=True):
        if not animate:
            plt.rcParams['text.usetex'] = True
        plt.style.use("dark_background")
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

        # Initialize the plots
        im1 = ax1.imshow(self.grid_data[0, :, :, :],cmap = 'plasma',vmin=np.min(self.loaded_grid), vmax=np.max(self.loaded_grid))
        im2 = ax2.imshow(self.entropy_states[0, :, :, :],cmap='viridis', vmin=1, vmax=np.max(self.loaded_states))

        # Optional: colorbars for ax1 and ax2
        cbar1 = fig.colorbar(im1, ax=ax1, label="Intensity", orientation="horizontal", pad=0.15, shrink = 0.75)
        cbar2 = fig.colorbar(im2, ax=ax2, label="Density States", orientation="vertical", pad=0.10, shrink = 0.75)

        ticks = np.linspace(1, 3281, 5)
        cbar2.set_ticks(ticks)

        # Set initial titles
        ax1.set_title("Grid Data")
        ax2.set_title("Density States")
        ax3.set_title("Entropy Change")
        ax1.axis("off")
        ax2.axis("off")
        if animate:
            def animate(frame):
                im1.set_data(self.grid_data[frame, :, :, :])
                im2.set_data(self.entropy_states[frame, :, :, :])
                ax3.plot(self.relative_entropy[:frame], color='r')

                # Optional: Update titles with frame number or other relevant info
                ax1.set_title(f"Grid Data - Frame: {frame}")
                ax2.set_title(f"Density States - Frame: {frame}")
                ax3.set_title(f"Entropy Change - Frame: {frame}")

            ani = FuncAnimation(fig, animate, frames=self.grid_data.shape[0], repeat=False, interval=80)
            plt.show()
        else:
            plt.show()

# check = PreChecks()
# check.animation_loop(animate=True)
"""
The Scene for a short video
Manim Section
Manim command for low quality: manim -p -ql Animations.py ImageFromArray 
Manim command for medium quality: manim -p -qm Animations.py ImageFromArray
Manim command for high quality: manim -p -qh Animations.py ImageFromArray
Note: your_class is changed to what class object you want to render
"""

class ImageFromArray(MovingCameraScene):
    def construct(self):
        ## First define all the variables and datas we require
        datas = setup()
        entropy_data = datas.relative_entrop
        the_grid = datas.grid
        the_states = datas.density_states
        Grid_images = datas.get_rgb_values(the_grid, 'plasma')
        State_images = datas.get_rgb_values(the_states, 'viridis')

        start, end, x_index,  _  = datas.entropy_setup()

        # Define the plot for the Manim graph
        entropy_axes = Axes(
            x_range=[0, 1600, 400],
            y_range = [0, 40, 5],
            x_length = 6,
            y_length = 3.5,
            axis_config={
                'include_numbers' : True,
                'tick_size' : 0.08,
            },
            tips= False
        )

        entropy_axes.to_edge(DOWN)
        entropy_axes.shift(RIGHT * 3)
        entropy_axes.scale(0.8)

        # Add x and y labels to the axis
        ylabel = entropy_axes.get_y_axis_label(
            Tex(r"Entropy $\Delta S \cdot 10^{3}/k_{b}$").scale(0.5).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.2,
        )
        xlabel = entropy_axes.get_x_axis_label(
            Tex("Iterations").scale(0.45), edge=DOWN, direction=DOWN, buff=0.10
        )

        # Create VGroups for the dots and line elements in Manim
        dot_elements = VGroup()
        line_elements = VGroup()

        GRID_HEIGHT = 7
        GRID_WIDTH = 6
        image_label, title, state_den_desc, Colorbar, state_colobar = None, None, None, None, None

        # Before the loop:
        Image = ImageMobject(Grid_images[0, :, :, :])
        Image.set(height=GRID_HEIGHT)
        Image.set(width=GRID_WIDTH)
        Image.to_edge(LEFT).shift(UP * 0.5 + LEFT * 0.5)

        Image_State = ImageMobject(State_images[0, :, :, :])
        Image_State.set(height=GRID_HEIGHT * 0.8)
        Image_State.set(width=GRID_WIDTH * 0.8)
        Image_State.shift(UP * 1.85 + RIGHT * 3)
        axes_drawn = False

        ## Save the camera state
        self.camera.frame.save_state()

        for i in range(1, len(x_index)):
            if i == 1:
                ## Define the Colorbar for the Grid
                Colorbar = ImageMobject(r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\colorbar.png")
                Colorbar.set(height=1)
                Colorbar.set(width=GRID_WIDTH)
                Colorbar.scale(0.8)
                Colorbar.next_to(Image, DOWN, aligned_edge=LEFT)

                ## Define the Colorbar for the Density of states
                state_colobar = ImageMobject(r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\state_colorbars.png")
                state_colobar.set(height=GRID_HEIGHT * 0.8)
                state_colobar.set(width=1)
                state_colobar.scale(0.75)
                state_colobar.next_to(Image_State, RIGHT, aligned_edge=RIGHT).shift(RIGHT * 0.5)

                self.play(FadeIn(Image, Colorbar))
                self.wait()

                ## Define the labels for the Grid
                image_label = Tex("Grid:").scale(0.6)
                image_label.next_to(Image, UP, aligned_edge=LEFT)

                title = Tex(r"This is a Cellular Automata grid").scale(0.75)
                title.to_corner(UP + LEFT)
                title.shift(LEFT * 0.5)

                self.play(Write(title), Write(image_label))
                self.wait(0.5)

                transform_title = Tex(r"Designed to show entropy increase").scale(0.75)
                transform_title.to_corner(UP + LEFT)
                transform_title.shift(LEFT * 0.5)

                ## Define the Labels for the Density of states Grid
                state_den_desc = Tex(r"Microstate Count:").scale(0.55)
                state_den_desc.next_to(Image_State, UP, aligned_edge=LEFT)

                self.play(Transform(title, transform_title))
                self.play(FadeIn(Image_State), FadeIn(state_colobar), Write(state_den_desc))

                if not axes_drawn:
                    self.play(
                        Create(entropy_axes),
                        Create(ylabel),
                        Create(xlabel),
                        run_time=1
                    )
                    axes_drawn = True

            ## Update Image Mobjects using previous states
            current_image = ImageMobject(Grid_images[i, :, :, :])
            current_image.set(height=GRID_HEIGHT)
            current_image.set(width=GRID_WIDTH)
            current_image.to_edge(LEFT).shift(UP * 0.5 + LEFT * 0.5)

            current_image_state = ImageMobject(State_images[i, :, :, :])
            current_image_state.set(height=GRID_HEIGHT * 0.80)
            current_image_state.set(width=GRID_WIDTH * 0.80)
            current_image_state.shift(UP * 1.85 + RIGHT * 3)

            dot = Dot(point=entropy_axes.coords_to_point(x_index[i - 1], entropy_data[i - 1]), radius=0.02)
            dot_elements.add(dot)

            if i > 1:
                line = Line(
                    entropy_axes.coords_to_point(x_index[i - 2], entropy_data[i - 2]),
                    entropy_axes.coords_to_point(x_index[i - 1], entropy_data[i - 1]),
                )
                line_elements.add(line)

            if i == 125:
                self.play(
                    self.camera.frame.animate.move_to(Image.get_center()).scale_to_fit_height(GRID_HEIGHT - 3.5),
                    AnimationGroup(
                        Transform(Image, current_image),
                        Transform(Image_State, current_image_state),
                        Create(dot),
                        lag_ratio=0.0
                    ),
                    run_time=1.75
                )

            elif 125 < i <= 160:
                self.play(
                    AnimationGroup(
                        Transform(Image, current_image),
                        Transform(Image_State, current_image_state),
                        Create(dot),
                        lag_ratio=0.5
                    ),
                    run_time=0.25
                )

            elif i == 161:
                self.play(
                    self.camera.frame.animate.restore(),
                    AnimationGroup(
                        Transform(Image, current_image),
                        Transform(Image_State, current_image_state),
                        Create(dot),
                        lag_ratio=0.5
                    ),
                    run_time=2.0
                )

            else:
                ## Transition the image from one frame to another.
                self.play(
                    Transform(Image, current_image), Transform(Image_State, current_image_state),
                    Create(dot),
                    run_time=0.1
                )


            if i == len(x_index) - 1:
                self.play(Create(line_elements), run_time=1.5)
                self.wait()
                self.play(FadeOut(entropy_axes, dot_elements, line_elements), FadeOut(ylabel, xlabel),
                          FadeOut(image_label, state_den_desc),
                          FadeOut(Image_State), FadeOut(Colorbar, state_colobar))

                ## New title
                new_title = Tex(r'The arrow of time')
                new_title.to_corner(UP + LEFT)

                self.play(FadeOut(Image),Transform(title, new_title), current_image.animate.scale(0.75))
                self.play(current_image.animate.shift(RIGHT * 7.10 + DOWN * 1.5))

                ## Create the arrow for the arrow of time.
                arrow_start_point = LEFT * 7
                arrow_end_point = RIGHT * 7
                arrow_shift = UP * 1.5
                arrow = Arrow(arrow_start_point, arrow_end_point, buff=0.1).shift(arrow_shift)

                # Update the arrow start and end points to reflect the shift
                arrow_start_point += arrow_shift
                arrow_end_point += arrow_shift

                dot1_fraction = 1.5 / 7.0
                dot2_fraction = 5.0 / 7.0

                dot1_location = interpolate(arrow_start_point, arrow_end_point, dot1_fraction)
                dot2_location = interpolate(arrow_start_point, arrow_end_point, dot2_fraction)

                dot1 = Dot(dot1_location)
                dot2 = Dot(dot2_location)

                before_label = Tex(r'Before').scale(0.6)
                after_label = Tex(r"After").scale(0.6)
                before_label.next_to(dot1, UP)
                after_label.next_to(dot2, UP)

                initial_image = ImageMobject(Grid_images[0, :, :, :])
                initial_image.match_height(current_image)
                initial_image.match_width(current_image)
                initial_image.next_to(current_image, LEFT).shift(LEFT * 2.25)

                self.play(Create(arrow), FadeIn(dot1, before_label), FadeIn(dot2, after_label), FadeIn(initial_image))

                grid1_top_left = initial_image.get_corner(UP + LEFT)
                grid1_top_right = initial_image.get_corner(UP + RIGHT)
                grid2_top_left = current_image.get_corner(UP + LEFT)
                grid2_top_right = current_image.get_corner(UP + RIGHT)

                line1_left = DashedLine(dot1.get_center(), grid1_top_left)
                line1_right = DashedLine(dot1.get_center(), grid1_top_right)
                line2_left = DashedLine(dot2.get_center(), grid2_top_left)
                line2_right = DashedLine(dot2.get_center(), grid2_top_right)

                self.play(Create(line1_left), Create(line1_right), Create(line2_left), Create(line2_right))
                self.wait(3)
                self.play(FadeOut(current_image), FadeOut(initial_image), Uncreate(arrow),
                          FadeOut(line1_left, line1_right, line2_left, line2_right),
                          FadeOut(dot1, dot2),
                          Uncreate(title),
                          Uncreate(before_label),
                          Uncreate(after_label))

        # Final self.wait() before doing anything else.
        self.wait()

