import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.cm
from manim import *
from scipy.special import comb
from scipy import signal
from scipy.ndimage import convolve
import random

class Setup:
    def __init__(self):
        self.grid_data = np.load(r'C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\grids.npy')
        self.prime_data = np.load(r'C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\prime_grids.npy')
        self.loaded_entropies = np.load(r'C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\entropies.npy')
        self.microstate_data = pd.read_csv(
            r"C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\Microstate_dataframe.csv")

        ## Get some class attibutes where the later Manim Scene can see
        self.Grid_copies = self.grid_data.shape[0]

    def get_rgb_values(self):
        RGB=np.array([self.convert_to_rgb_image(self.grid_data[i, :, :],
                                                                 cmap=plt.get_cmap("plasma")) for i in range(self.Grid_copies)])
        Gird= RGB[0, :, :, 0] / 255
        return RGB, Gird

    def convert_to_rgb_image(self, grid_data, cmap="plasma", vmin=0, vmax=16):
        self.cmap = matplotlib.colormaps.get_cmap(cmap)
        self.norm = plt.Normalize(vmin, vmax)
        self.grid_data_rgb = self.cmap(self.norm(grid_data))
        return (self.grid_data_rgb[:, :, :3] * 255).astype(np.uint8)

    def setup(self, *kwargs):
        start = 0
        stop = (self.grid_data.shape[0] - 1) * 4
        step = 4
        entropy = np.array(self.loaded_entropies)
        x_index = np.arange(start, stop + step, step)

        return start, stop, x_index, entropy

class Function:
    def __init__(self):
        pass

    def initialize_grid(self, lengths: int, choice: str, limit: int):
        length = lengths
        grid = np.pad(np.zeros((length, length)), pad_width=1, mode='constant', constant_values=8)
        if choice == "rectangle":
            x, y = int(length / 2), int(length / 2)
            z = int(0.35 * x)
            w = int(0.5 * y)
            grid[x: x + z, y: y + w] = limit
        elif choice == "circle":
            center = ((length / 2), (length / 2))
            radius = int(math.sqrt(0.08 * length ** 2 / math.pi))
            x, y = np.meshgrid(np.linspace(0, length + 2, length + 2), np.linspace(0, length + 2, length + 2))
            distance = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
            grid[distance <= radius] = limit

        return grid.astype(int)

    def apply_rules_2d(self, grid, heat_transfer_probability, temperature):
        max_val = np.max(grid[1:-1, 1:-1])
        non_zero_cells = np.where(grid[1:-1, 1:-1] >= 1)  ## Only find tuples where the non_zero_cells are
        # Random assortment of non_zero_cells locations while maintaining correspondance between rows and columns
        indices = np.arange(len(non_zero_cells[0]))
        np.random.shuffle(indices)
        non_zero_cells = (non_zero_cells[0][indices], non_zero_cells[1][indices])
        direction_vector = np.array([[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]])

        for i in range(len(non_zero_cells[0])):  ## For every non-zero cell
            row, col = non_zero_cells[0][i] + 1, non_zero_cells[1][i] + 1  ## get the x and y axis or positions

            if np.random.rand() < heat_transfer_probability:
                ## Choose which direction it can go
                ## Check whats happening on all 8 sides of a non-zero cell
                neighbors = np.array(
                    [grid[(row - 1), (col - 1)], grid[(row), (col - 1)], grid[(row + 1), (col - 1)],
                     grid[(row + 1), (col)],
                     grid[(row + 1), (col + 1)],
                     grid[(row), (col + 1)],
                     grid[(row - 1), (col + 1)], grid[(row - 1), (col)]])

                difference = np.array([max_val - grid[(row - 1), (col - 1)],
                                       max_val - grid[(row), (col - 1)],
                                       max_val - grid[(row + 1), (col - 1)],
                                       max_val - grid[(row + 1), (col)],
                                       max_val - grid[(row + 1), (col + 1)],
                                       max_val - grid[(row), (col + 1)],
                                       max_val - grid[(row - 1), (col + 1)],
                                       max_val - grid[(row - 1), (col)]
                                       ])
                ## If all the surroundings of a 8 cell is occupied, do nothing
                if np.all(neighbors == max_val) == True:
                    pass
                ## Else select only the lists within direction_vector_array that matches with the truth values of neighbors
                ## If neighbors==0 select True and randomly select what is available within direction_vector
                else:
                    boolean_dir_index = (neighbors <= max_val - 1)
                    valid_directions = direction_vector[boolean_dir_index]
                    delta_E = difference[boolean_dir_index]
                    ### Applying the boltzmann factor to modify probabilities based on energy difference to a 8.
                    energy_diff = np.abs(delta_E)
                    boltzmann_factors = np.exp(energy_diff * (1 / temperature))
                    partition_function = np.sum(boltzmann_factors)
                    direction_probabilities = boltzmann_factors / partition_function
                    cumsum_probs = np.cumsum(direction_probabilities)
                    sampling = np.random.rand()
                    dir_indexing = np.searchsorted(cumsum_probs, sampling)
                    possible_directions = valid_directions[dir_indexing]
                    grid[(row + possible_directions[0], col + possible_directions[1])] += 1
                    grid[row, col] -= 1
        return grid

class check_grid:
    def __init__(self, yes=False):
        self.animation=yes
        self.SETUP=Setup()
        self.Grid_data=self.SETUP.grid_data
        self.Prime_data=self.SETUP.prime_data

    def Animation(self):
        if self.animation==True:

            plt.style.use("dark_background")
            fig, (ax, ax2)=plt.subplots(1,2, figsize=(10,5), width_ratios=[1.2, 0.98])

            im=ax.imshow(self.Grid_data[0, :, :], cmap="plasma", vmin=np.min(self.Grid_data[0, :, :]), vmax=np.max(self.Grid_data[0, :, :]))
            im2=ax2.imshow(self.Prime_data[0, :, :], cmap="binary", vmin=0, vmax=1)
            fig.colorbar(im, ax=ax, label="Intensity", shrink=0.56)

            ax.axis("off")
            ax2.axis("off")

            def animate(frame):
                im.set_data(self.Grid_data[frame, :, :])
                im2.set_data(self.Prime_data[frame, :, :])

                ax.set_title(f"Temp: {1.0}", loc="left")
                ax.set_title(f"Epoch: {frame}", loc="right")
                ax2.set_title("Non-Prime locations")

            ani=FuncAnimation(fig,animate, frames=self.Grid_data.shape[0], repeat=False, interval=80)
            plt.show()

        else:
            pass

bug_checking=check_grid(yes="no")
bug_checking.Animation()

"""
Scene 1: Grid simulation
Manim Section
Manim command for low quality: manim -p -ql Manimations.py ImageFromArray 
Manim command for medium quality: manim -p -qm Manimations.py ImageFromArray
Manim command for high quality: manim -p -qh Manimations.py ImageFromArray
Note: your_class is changed to what class object you want to render
"""
class ImageFromArray(Scene):
    def construct(self):
        ## Define the variables and data needed first
        Datas=Setup()
        Grid_data_rgb, Gird=Datas.get_rgb_values()
        start, end, x_index, entropy = Datas.setup()
        # Create axes for the graph
        axes = Axes(
            x_range=[0, 1600, 400],  # [start, stop, step]
            y_range=[145, 180, 5],
            x_length=5.5,
            y_length=4,
            axis_config={
                "include_numbers": True,
                "tick_size": 0.08,
            },
            tips=False
        )
        axes.to_edge(RIGHT)

        # Add x and y axis labels
        ylabel = axes.get_y_axis_label(
            Tex("Entropy $S.10^{3}/k_{b}$").scale(0.5).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT,
            buff=0.2,
        )
        xlabel = axes.get_x_axis_label(
            Tex("Epochs").scale(0.5), edge=DOWN, direction=DOWN, buff=0.2
        )

        # Create VGroups for dots and lines separately
        dot_elements = VGroup()
        line_elements = VGroup()

        current_image = None
        for i in range(1, len(x_index)):
            axes_drawn = False
            if i == 1:
                Image = ImageMobject(Grid_data_rgb[0, :, :, :])
                Image.set(height=4)
                Image.set(width=5.5)
                Image.to_edge(LEFT)

                Colorbar = ImageMobject(r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\colorbar.png")
                Colorbar.set(height=1)
                Colorbar.set(width=5)
                Colorbar.next_to(Image, DOWN, aligned_edge=LEFT)

                self.play(FadeIn(Image, Colorbar))
                self.wait()
                current_image = Image

                image_label = Tex("Grid:")
                image_label.next_to(Image, UP, aligned_edge=LEFT)

                title = Tex(r"This is a Cellular Automata grid")
                title.to_corner(UP + LEFT)

                self.play(Write(title), Write(image_label))

                self.wait(2)
                transform_title = Tex(r"Designed to show entropy increase")
                transform_title.to_corner(UP + LEFT)
                self.play(Transform(title, transform_title))
            else:
                Image = ImageMobject(Grid_data_rgb[i - 1, :, :, :])
                Image.set(height=4)
                Image.set(width=5.5)
                Image.to_edge(LEFT)

            current_image = ImageMobject(Grid_data_rgb[i, :, :, :])
            current_image.set(height=4)
            current_image.set(width=5.5)
            current_image.to_edge(LEFT)

            dot = Dot(point=axes.coords_to_point(x_index[i - 1], entropy[i - 1]), radius=0.02)
            dot_elements.add(dot)

            if i == 1:
                if not axes_drawn:
                    self.play(
                        Create(axes),
                        Create(ylabel),
                        Create(xlabel),
                        run_time=1
                    )
                    axes_drawn = True

            if i > 1:
                line = Line(
                    axes.coords_to_point(x_index[i- 2], entropy[i - 2]),
                    axes.coords_to_point(x_index[i - 1], entropy[i - 1]),
                )
                line_elements.add(line)

            self.play(
                Transform(Image, current_image),
                Create(dot),  # Play the Create animation for the current dot only
                run_time=0.1)

            if i == len(x_index)-1:
                self.play(Create(line_elements), run_time=1.5)
                self.wait()

        self.wait()

        # Create a black rectangle with the same dimensions as the screen
        black_rect = Rectangle(fill_color=BLACK, fill_opacity=1, stroke_opacity=0, width=20, height=25)
        self.play(FadeIn(black_rect, run_time=2))
        self.wait()
"""
Scene 2: Defining the microstate
To activate the CoinTossTree code write into the command promt
manim - qh CoinTossTree
"""


class CoinTossTree(MovingCameraScene):
    DEPTH = 4
    CHILDREN_PER_VERTEX = 2
    LAYOUT_CONFIG = {"vertex_spacing": (0.6, 0.9)}

    HEAD_VERTEX_CONF = {"radius": 0.1, "color": BLUE_B, "fill_opacity": 1.0}
    TAIL_VERTEX_CONF = {"radius": 0.1, "color": RED_B, "fill_opacity": 1.0}
    ROOT_VERTEX_CONF = {"radius": 0.15, "color": WHITE, "fill_opacity": 1.0}

    def construct(self):
        script = Tex(r"To understand, we would need to introduce some terms", font_size=40)
        self.play(
            Write(script)
        )
        self.wait(2)

        script2 = Tex("Grappling with microstates, to lay our foundations firm", font_size=40)
        script2.to_corner(UP + LEFT)
        self.play(
            Transform(script, script2),
        )
        self.wait(2)

        script3 = Tex("Let us consider a game of coins")
        script3.to_corner(UP + LEFT)

        self.play(
            FadeOut(script),
            FadeIn(script3, shift=DOWN)
        )

        self.wait(2)

        script4 = Tex("By employing a tree with its lines conjoined")
        script4.to_corner(UP + LEFT)

        g = Graph([""], [], vertex_config=self.ROOT_VERTEX_CONF)
        g = self.expand_vertex(g, "", 1)
        self.add(g)

        self.play(
            (g.animate.change_layout(
                "tree",
                root_vertex="",
                layout_config=self.LAYOUT_CONFIG)), FadeOut(script3), FadeIn(script4, shift=DOWN))

        # Gradually zoom out to the specified width and height

        self.play(self.camera.frame.animate.set(width=18, height=10), run_time=1.5)
        self.play(g.animate.shift(LEFT * 4.0), run_time=1.0)

        # Add the legend with smaller text size and adjusted position
        head_label = Tex("Heads:", color=RED_B, font_size=40)
        head_circle = Circle(radius=0.1, color=RED_B, fill_opacity=1.0)
        tail_label = Tex("Tails:", color=BLUE_B, font_size=40)
        tail_circle = Circle(radius=0.1, color=BLUE_B, fill_opacity=1.0)

        head_label.next_to(head_circle, LEFT)
        tail_label.next_to(tail_circle, LEFT)

        legend = VGroup(head_label, head_circle).arrange_submobjects(RIGHT, buff=0.4)
        legend2 = VGroup(tail_label, tail_circle).arrange_submobjects(RIGHT, buff=0.4)

        legend.to_corner(DOWN + LEFT, buff=0.5).shift(UP * 0.5)
        legend2.next_to(legend, buff=0.5)

        self.play(FadeIn(legend), FadeIn(legend2))
        branches_to_highlight = [
            ["T", "T", "T", "T"],
            ["T", "T", "T", "H"],
            ["T", "T", "H", "T"],
            ["T", "T", "H", "H"],
            ["T", "H", "T", "T"],
            ["T", "H", "T", "H"],
            ["T", "H", "H", "T"],
            ["T", "H", "H", "H"],
            ["H", "T", "T", "T"],
            ["H", "T", "T", "H"],
            ["H", "T", "H", "T"],
            ["H", "T", "H", "H"],
            ["H", "H", "T", "T"],
            ["H", "H", "T", "H"],
            ["H", "H", "H", "T"],
            ["H", "H", "H", "H"],
        ]

        reversed_branch = branches_to_highlight[::-1]

        script5 = Tex("We can list the paths as shown below: ")
        script5.to_corner(UP + LEFT)

        description = Tex("Configurations:", font_size=40)
        description.to_corner(UP + RIGHT).shift(DOWN * 1.3)
        description.shift(LEFT * 2.5)
        self.play(FadeIn(description), Transform(script4, script5))
        self.wait()

        configurations = [f"{idx + 1}: {''.join(config)}" for idx, config in enumerate(reversed_branch)]

        configuration_tex = [self.create_configuration_tex(config) for config in configurations]

        configuration_grid = VGroup(*configuration_tex[:8]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        configuration_grid2 = VGroup(*configuration_tex[8:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        configuration_grid2.next_to(configuration_grid, RIGHT, buff=1.5)

        # Shift the grids to desired positions
        configuration_grid.next_to(g, RIGHT, buff=1.5).shift(LEFT * 0.8)  # Adjust the shift values as needed
        configuration_grid2.shift(RIGHT * 2.0)  # Adjust the shift values as needed

        configuration_grid.shift(DOWN * 1)
        configuration_grid2.shift(DOWN * 1)

        self.play(FadeIn(configuration_grid), FadeIn(configuration_grid2))

        self.wait()

        script6 = Tex("By highlighting the routes we'd like to know")
        script6.to_corner(UP + LEFT)
        self.play(
            FadeOut(script4),
            FadeIn(script6, shift=DOWN)
        )
        self.wait()

        self.highlight_branches(g, branches_to_highlight, configuration_grid, configuration_tex)
        self.wait()

        script7 = Tex("Each of these routes, a microstate it is")
        script7.to_corner(UP + LEFT)

        description2 = Tex("Microstates: ", font_size=40)
        description2.to_corner(UP + RIGHT).shift(DOWN * 1.3)
        description2.shift(LEFT * 2.5)

        self.play(Transform(description, description2), Transform(script6, script7))
        self.wait()

        script8 = Tex("Concluding all the premises that there is").set_color(BLACK)
        script8.to_corner(UP + LEFT)
        self.play(FadeOut(script6), FadeIn(script8))
        self.play(script8.animate.set_color(WHITE))

        self.wait(2)

        black_rect = Rectangle(fill_color=BLACK, fill_opacity=1, stroke_opacity=0, width=22, height=14)
        self.play(FadeIn(black_rect, run_time=2))
        self.wait()

    def expand_vertex(self, g, vertex_id: str, depth: int):
        coin_sides = ["H", "T"]
        new_vertices = [f"{vertex_id}{side}" for side in coin_sides]
        new_edges = [(vertex_id, child_id) for child_id in new_vertices]

        for side, child_id in zip(coin_sides, new_vertices):
            vertex_conf = self.HEAD_VERTEX_CONF if side == "H" else self.TAIL_VERTEX_CONF
            g.add_edges(
                (vertex_id, child_id),
                vertex_config=vertex_conf,
                positions={
                    child_id: g.vertices[vertex_id].get_center() + 0.1 * DOWN
                },
            )

        if depth < self.DEPTH:
            for child_id in new_vertices:
                self.expand_vertex(g, child_id, depth + 1)

        return g

    def highlight_vertex(self, g, vertex_id):
        # Find the corresponding vertex
        vertex = g.vertices[vertex_id]

        # Scale up the vertex
        self.play(vertex.animate.scale(1.5), run_time=0.04)

        # Return a function to reset the scale
        def reset_scale():
            self.play(vertex.animate.scale(1 / 1.5), run_time=0.04)

        return reset_scale

    def highlight_branches(self, g, branches, configuration_grid, configuration_tex):
        def update_table(index):
            for _ in range(1):
                self.play(FadeIn(configuration_tex[index], run_time=0.1))
                self.play(FadeOut(configuration_tex[index], run_time=0.1))
            self.play(FadeIn(configuration_tex[index], run_time=0.1))

        for index, branch in enumerate(branches):
            path_to_vertex = "".join(branch)
            path_ids = [""]
            for side in path_to_vertex:
                path_ids.append(path_ids[-1] + side)

            # Exclude the root vertex from highlighting
            path_ids = path_ids[1:]

            reset_scale_funcs = []

            for current_vertex_id in path_ids:
                vertex = g.vertices[current_vertex_id]
                reset_scale_funcs.append(self.highlight_vertex(g, current_vertex_id))

            self.wait(0.15)

            update_table(index)

            for current_vertex_id, reset_scale in zip(path_ids, reset_scale_funcs):
                reset_scale()

    def create_configuration_tex(self, config_text):
        tex_id = MathTex(r"\text{" + config_text.split(':')[0] + r"}", color=WHITE, font_size=40)
        config = config_text.split(':')[1].strip()
        tex_config = VGroup(
            *[MathTex(r"\text{" + letter + r"}", color=RED_B if letter == "H" else BLUE_B, font_size=40) for letter in
              config])
        spaced_tex_config = VGroup(*tex_config).arrange(RIGHT, buff=0.3)
        return VGroup(tex_id, MathTex(r"\text{:}", color=WHITE, font_size=40), spaced_tex_config).arrange(RIGHT,
                                                                                                          buff=0.4)
"""
Macrostate: Scene 2 
To call this function use manim - qh MacroStateScene
"""

class MacroStateScene(MovingCameraScene):
    def construct(self):
        script1 = Tex(r"But the sea is vast that there is more to know", font_size=40)
        self.play(Write(script1))

        self.wait(0.8)

        script2 = Tex(r"The macrostate that I've yet to show", font_size=40)
        self.play(
            Transform(script1, script2),
        )
        self.wait(0.8)

        script3 = Tex(r"Let's bring the table back to the stage", font_size=40)
        script3.to_corner(UP + LEFT).shift(LEFT * 1.5)

        self.play(
            FadeOut(script1),
            FadeIn(script3, shift=DOWN),
            self.camera.frame.animate.set(width=30, height=10), run_time=1.0)

        self.wait()

        branches_to_highlight = [
            ["T", "T", "T", "T"],
            ["T", "T", "T", "H"],
            ["T", "T", "H", "T"],
            ["T", "T", "H", "H"],
            ["T", "H", "T", "T"],
            ["T", "H", "T", "H"],
            ["T", "H", "H", "T"],
            ["T", "H", "H", "H"],
            ["H", "T", "T", "T"],
            ["H", "T", "T", "H"],
            ["H", "T", "H", "T"],
            ["H", "T", "H", "H"],
            ["H", "H", "T", "T"],
            ["H", "H", "T", "H"],
            ["H", "H", "H", "T"],
            ["H", "H", "H", "H"],
        ]

        reversed_branch = branches_to_highlight[::-1]

        configurations = [f"{idx + 1}: {''.join(config)}" for idx, config in enumerate(reversed_branch)]

        configuration_tex = [self.create_configuration_tex(config) for config in configurations]

        configuration_grid = VGroup(*configuration_tex[:8]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        configuration_grid2 = VGroup(*configuration_tex[8:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        configuration_grid2.next_to(configuration_grid, RIGHT, buff=1.5)

        configuration_grid.shift(LEFT * 7.0)
        configuration_grid2.shift(LEFT * 8.0)

        configuration_grid.scale(0.8)
        configuration_grid2.scale(0.8)
        self.play(FadeIn(configuration_grid), FadeIn(configuration_grid2))

        self.wait()

        script4 = Tex(r"And classify them by the heads they make", font_size=40)
        script4.to_corner(UP + LEFT).shift(LEFT * 1.5)
        self.play(Transform(script3, script4))

        templates, data = self.create_table()
        Table = Tex(data, tex_template=templates).scale(0.65)
        Table.shift(RIGHT * 3.5)
        self.play(Write(Table))

        self.wait(1.5)

        script5 = Tex(r"Each of this classes is a macrostate")
        script5.to_corner(UP + LEFT).shift(LEFT * 1.5)
        self.play(FadeOut(script3),
                  FadeIn(script5, shift=DOWN),
                  FadeOut(configuration_grid),
                  FadeOut(configuration_grid2),
                  Table.animate.shift(LEFT * 4.0)
                  )
        self.wait()

        ## Equation for the Boltzmann entropy
        eq1 = MathTex("S = k_{b} \log(\Omega)").shift(UP * 1.5)
        eq2 = MathTex("{S}/{k_{b}} = \log(\Omega)").shift(UP * 1.5)

        self.play(Table.animate.shift(DOWN * 1))
        self.play(Write(eq1))
        self.play(TransformMatchingShapes(eq1, eq2))
        self.wait()

        script6 = Tex(r"And we can compute the entropy for boltzmann's sake")
        script6.to_corner(UP + LEFT).shift(LEFT * 1.5)

        Entropy_code = r"""
            \begin{tabular}{ p{1.5cm}p{1.5cm}p{2.7cm} }
                \textbf{Heads} & \textbf{$\Omega$} & \textbf{Entropy $S/k_{b}$}\\
                 0   & 1 & 0\\
                 1 &   4 & 1.39\\
                 2 & 6  & 1.79 \\
                 3 & 4 & 1.39\\
                 4 & 1 & 0\\
            \end{tabular}
        """

        Entropy_table = Tex(Entropy_code, tex_template=templates).scale(0.9).shift(DOWN * 1)
        self.play(Transform(Table, Entropy_table), Transform(script5, script6), run_time=1.5)
        self.wait(2.5)
        black_rect = Rectangle(fill_color=BLACK, fill_opacity=1, stroke_opacity=0, width=30, height=20)
        self.play(FadeIn(black_rect, run_time=1.5))
        self.wait()

    def create_configuration_tex(self, config_text):
        tex_id = MathTex(r"\text{" + config_text.split(':')[0] + r"}", color=WHITE, font_size=40)
        config = config_text.split(':')[1].strip()
        tex_config = VGroup(
            *[MathTex(r"\text{" + letter + r"}", color=RED_B if letter == "H" else BLUE_B, font_size=40) for letter in
              config])
        spaced_tex_config = VGroup(*tex_config).arrange(RIGHT, buff=0.3)
        return VGroup(tex_id, MathTex(r"\text{:}", color=WHITE, font_size=40), spaced_tex_config).arrange(RIGHT,
                                                                                                          buff=0.4)

    def create_table(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{array}")
        template.add_to_preamble(r"\usepackage{xcolor}")

        LaTeX_code = r"""
            \begin{tabular}{*{5}{>{\centering\arraybackslash}p{1.7cm}}}
              && \textcolor{blue}{T} \textcolor{blue}{T} \textcolor{red}{H} \textcolor{red}{H} \\

              && \textcolor{red}{H} \textcolor{red}{H} \textcolor{blue}{T} \textcolor{blue}{T} \\

              & \textcolor{blue}{T} \textcolor{blue}{T} \textcolor{red}{T} \textcolor{blue}{H} & 
              \textcolor{blue}{T} \textcolor{red}{H} \textcolor{red}{H} \textcolor{blue}{T} &
              \textcolor{blue}{T} \textcolor{red}{H} \textcolor{red}{H} \textcolor{red}{H} \\

              & \textcolor{blue}{T} \textcolor{red}{T} \textcolor{blue}{H} \textcolor{blue}{T} & 
              \textcolor{red}{H} \textcolor{blue}{T} \textcolor{blue}{T} \textcolor{red}{H} &
              \textcolor{red}{H} \textcolor{blue}{T} \textcolor{red}{H} \textcolor{red}{H} \\

              & \textcolor{red}{T} \textcolor{blue}{H} \textcolor{blue}{T} \textcolor{red}{T} &
              \textcolor{red}{H} \textcolor{blue}{T} \textcolor{red}{H} \textcolor{blue}{T} & 
              \textcolor{red}{H} \textcolor{red}{H} \textcolor{blue}{T} \textcolor{red}{H} \\ 

               \textcolor{blue}{T} \textcolor{blue}{T} \textcolor{blue}{T} \textcolor{blue}{T} &
               \textcolor{blue}{H} \textcolor{blue}{T} \textcolor{blue}{T} \textcolor{red}{T} & 
               \textcolor{blue}{T} \textcolor{red}{H} \textcolor{blue}{T} \textcolor{red}{H} & 
               \textcolor{red}{H} \textcolor{red}{H} \textcolor{red}{H} \textcolor{blue}{T} & 
               \textcolor{red}{H} \textcolor{red}{H} \textcolor{red}{H} \textcolor{red}{H} \\

               \\
               \textbf{0 H's} & \textbf{1 H's} & \textbf{2 H's} & \textbf{3 H's} & \textbf{4 H's} \\
              \textbf{1} & \textbf{4} & \textbf{6} & \textbf{4} & \textbf{1} \\
              \\
            \end{tabular}
        """

        return template, LaTeX_code


"""
Macrostate: Scene 3 
To call this function use manim - qh MacroStateScaledScene
"""

class MacroStateScaledScene(MovingCameraScene):
    def construct(self):
        ## Script scenes
        script1 = Tex(r"The example's lame, you might say ", font_size=45)
        self.play(Write(script1))
        self.wait(0.8)

        script2 = Tex(r"Just scale the game and let it play", font_size=45)
        self.play(Transform(script1, script2))
        self.wait(0.8)

        script3 = Tex(r"Now you'll see what's at stake", font_size=45)
        script3.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 0.5)

        ## Coin scenes
        coin_grid = VGroup()
        box = RoundedRectangle(width=7.8, height=7.8, color="#DC143C")
        box.move_to([3.125, 0, 0])
        coin_grid.add(box)

        coins_pos = [(0.75 * x - 1, 0.75 * y - 2.0 + 0.125, 0) for x in range(1, 11) for y in range(-2, 8)]
        coins = [Circle(radius=0.25, color=BLUE_B, fill_opacity=1, stroke_width=5) for k in range(len(coins_pos))]
        coin_array = self.generate_coin_array()

        for coin, pos in zip(coins, coins_pos):
            coin.move_to(pos)
            coin_grid.add(coin)

        # Add the group to the scene
        self.add(coin_grid)
        coin_grid.shift(UP * 0.5).shift(RIGHT * 0.7)

        # Animate first the coin grid and etc
        self.play(FadeIn(coin_grid), self.camera.frame.animate.set(width=25, height=10), FadeOut(script1),
                  FadeIn(script3, shift=DOWN), run_time=2.0)
        self.wait()

        ## Script 4 to change the text while animatiing the coins
        script4 = Tex(r"Billions of ways per macrostate")
        script4.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)

        Table_TeX = r"""
        \begin{tabular}{ |p{1.5cm}|p{1.5cm}| p{2.7cm}| }
            \hline
            \textbf{Heads} & \textbf{$\Omega$} & \textbf{Entropy $S/k_{b}$}\\
            \hline
             0   & 1 & 0\\
             2 & 4950 & 8.5\\
             5 & $10^{7}$  & 16.1 \\
             10 & $10^{13}$ & 29.9\\
             20 & $10^{20}$ & 46.1 \\
             30 & $10^{25}$  & 57.6  \\
             40 & $10^{28}$  & 64.5  \\
             50 & $10^{29}$  & 66.8  \\
             60 & $10^{28}$   & 64.5  \\
             70 & $10^{25}$  & 57.6  \\
             80 & $10^{20}$  & 46.1  \\
             90 & $10^{13}$  & 29.9  \\
             95 & $10^{7}$  & 16.1  \\
             98 & 4950  & 8.5  \\
             100 & 1  &  0 \\
             \hline
        \end{tabular}
        """
        Config_Table = Tex(Table_TeX).scale(0.7).shift(LEFT * 4).shift(UP * 0.4)

        # Flip all coins according to the generated coin array for 20 iterations
        for i in range(15):
            coin_array = self.generate_coin_array()
            flip_animations = self.create_flip_animations(coins, coin_array)
            if i == 0:
                self.play(Write(Config_Table), Transform(script3, script4), run_time=1.5)
                self.play(*flip_animations, run_time=0.8)
            else:
                self.play(*flip_animations, run_time=0.5)

        self.wait(1.5)

        script5 = Tex(r"Now imagine this with all your mates ")
        script5.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)

        self.play(FadeIn(script5, shift=DOWN), FadeOut(script3), FadeOut(Config_Table),
                  coin_grid.animate.shift(DOWN * 0.8))
        self.play(coin_grid.animate.shift(LEFT * 7.5), self.camera.frame.animate.set(width=20, height=12))
        self.wait()

        script6 = Tex(r"A system in motion with random states")
        script6.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)
        self.play(FadeOut(script5), FadeIn(script6, shift=DOWN), run_time=1.5)

        script7 = Tex(r"Which is likelier you should query")
        script7.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)

        ## 2nd for loop animation for flipping coins
        for k in range(15):
            coin_array = self.generate_coin_array()
            flip_animations = self.create_flip_animations(coins, coin_array)
            if k == 7:
                self.play(*flip_animations, Transform(script6, script7), run_time=1.0)
            else:
                self.play(*flip_animations, run_time=0.5)

        script8 = Tex(r"All heads")
        script8.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)

        script9 = Tex(r"Or Tails")
        script9.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)

        script10 = Tex(r"Or mixed uniformly")
        script10.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)

        ## Flip the coin according to the script
        # Coin array for ALL HEADS
        coin_array = self.generate_all_heads()
        flip_ani = self.create_flip_animations(coins, coin_array)
        self.play(*flip_ani, FadeOut(script6), FadeIn(script8, shift=DOWN))

        ## Coin array for ALL TAILS
        coin_array = self.generate_all_tails()
        flip_ani = self.create_flip_animations(coins, coin_array)
        self.play(*flip_ani, FadeOut(script8), FadeIn(script9, shift=DOWN))

        ## Coin array for all Uniform
        for j in range(12):
            coin_array = self.generate_coin_array()
            flip_animations = self.create_flip_animations(coins, coin_array)
            if j == 0:
                self.play(*flip_animations, FadeOut(script9), FadeIn(script10, shift=DOWN))
            else:
                self.play(*flip_animations, run_time=0.5)

        self.wait()

        script11 = Tex(r"Lets bring back the main equation ")
        script11.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)

        script12 = Tex(r"And see the states that matches the occasion")
        script12.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)

        Boltzmann_entropy = MathTex("S = k_{b} \log(\Omega)")
        Boltzmann_entropy.shift(RIGHT * 3.2).shift(UP * 3)

        self.play(FadeOut(script10), FadeIn(script11, shift=DOWN), FadeIn(Boltzmann_entropy))
        self.wait()

        ## Entropy real-time calculation
        current_heads = np.sum(coin_array)
        current_entropy = self.compute_entropy(current_heads)
        entropy_label = Tex(r"Entropy: {:.2f}".format(current_entropy))
        entropy_label.shift(RIGHT * 3.2)
        heads_label = Tex(r"Heads: {}".format(current_heads))
        heads_label.shift(RIGHT * 3.2).shift(DOWN * 1)

        self.play(Transform(script11, script12), FadeIn(entropy_label),
                  FadeIn(heads_label))
        self.wait()

        script13 = Tex(r"Now you see why entropy grows")
        script13.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)

        script14 = Tex(r"As there is more routes for it to flow")
        script14.to_corner(UP + LEFT).shift(UP * 1).shift(LEFT * 1.0)

        ## Loop for final animation
        for o in range(30):
            if o == 12:
                coin_array = self.generate_coin_array()
                flip_animations = self.create_flip_animations(coins, coin_array)
                self.play(*flip_animations, FadeOut(script11), FadeIn(script13))

                # Update the text labels
                num_heads = np.sum(coin_array)
                entropy = self.compute_entropy(num_heads)
                self.update_labels(entropy_label, heads_label, entropy, num_heads)
            elif o == 16:
                coin_array = self.generate_coin_array()
                flip_animations = self.create_flip_animations(coins, coin_array)
                self.play(*flip_animations, Transform(script13, script14))

                # Update the text labels
                num_heads = np.sum(coin_array)
                entropy = self.compute_entropy(num_heads)
                self.update_labels(entropy_label, heads_label, entropy, num_heads)
            else:
                coin_array = self.generate_coin_array()
                flip_animations = self.create_flip_animations(coins, coin_array)
                self.play(*flip_animations, run_time=0.5)

                # Update the text labels
                num_heads = np.sum(coin_array)
                entropy = self.compute_entropy(num_heads)
                self.update_labels(entropy_label, heads_label, entropy, num_heads)

        self.wait()
        black_rect = Rectangle(fill_color=BLACK, fill_opacity=1, stroke_opacity=0, width=35, height=25)
        self.play(FadeIn(black_rect, run_time=1.0))
        self.wait()

    def generate_coin_array(self):
        return np.random.randint(0, 2, size=(10, 10))

    def generate_all_heads(self):
        s = (10, 10)
        array = np.zeros(s, dtype=int)
        return array

    def generate_all_tails(self):
        s = (10, 10)
        array = np.ones(s, dtype=int)
        return array

    def create_flip_animations(self, coins, coin_array):
        animations = []
        for i, coin in enumerate(coins):
            x, y = i % 10, i // 10
            next_color = RED_B if coin_array[y, x] == 0 else BLUE_B
            if coin.get_color() != next_color:
                anim = coin.animate.rotate(180 * DEGREES, axis=RIGHT).scale(np.array([0.01, 1, 1])).rotate(
                    180 * DEGREES, axis=RIGHT).scale(np.array([100, 1, 1])).set_color(next_color).set_fill(next_color)
                animations.append(anim)
        return animations

    def compute_entropy(self, num_heads):
        num_tails = 100 - num_heads
        num_combinations = comb(100, num_heads)
        entropy = np.log(num_combinations)
        return entropy

    def update_labels(self, entropy_label, heads_label, entropy, num_heads):
        entropy_label.become(Tex(r"Entropy: {:.2f}".format(entropy)).shift(RIGHT * 3.2))
        heads_label.become(Tex(r"Heads: {}".format(num_heads)).shift(RIGHT * 3.2).shift(DOWN * 1))

"""
Scene 4: The first law of thermodynamics
call this function on Pycharm's command promt: manim -p -qh Manimations.py BinaryFirstLaw
"""

class BinaryFirstLaw(MovingCameraScene):
    def construct(self):
        """
        First branch of the animation says the script needed to explain the animations below.
        Second branch of the animation tells python what to do to run the animations.

        """
        Title = Tex("First Law of thermodynamics")
        Title.to_corner(UP + LEFT)

        Title_Underline = Underline(Title, buff=0.15)

        First_law_thermodynamics = Tex("Energy cannot be created or destroyed", font_size=38).shift(UP * 1)
        First_law_eq = MathTex("\Delta U = \Delta Q + \Delta W", font_size=40)

        script2 = Tex("For an isolated system : ", font_size=35).shift(UP * 1)

        self.play(FadeIn(Title), FadeIn(Title_Underline),
                  FadeIn(First_law_thermodynamics), Write(First_law_eq))
        self.wait()

        self.play(Transform(First_law_thermodynamics, script2))

        Constant_eq = MathTex("\Delta U = 0", font_size=42)

        self.play(TransformMatchingShapes(First_law_eq, Constant_eq), run_time=1.5)
        self.wait()

        Title2 = Tex(r"Building on abstraction: ")
        Title2.to_corner(UP + LEFT)
        Title2_underline = Underline(Title2, buff=0.15)

        script3 = Tex("Consider 2 binary systems: ", font_size=40)
        script3.to_corner(LEFT).shift(UP * 1.5)

        s_1, s_2 = self.generate_subsystems(6, 7)

        string1 = r"$s_{1}= $" + str(s_1)
        string2 = r"$s_{2}= $" + str(s_2)

        System_one = Tex(string1, font_size=40).to_corner(LEFT).shift(UP * 0.8)
        System_two = Tex(string2, font_size=40).to_corner(LEFT)

        self.play(Transform(Title, Title2), FadeOut(First_law_thermodynamics),
                  FadeIn(script3),
                  Write(System_one), Write(System_two),
                  FadeOut(Constant_eq), Transform(Title_Underline, Title2_underline), run_time=1.5)

        self.wait()

        script4 = Tex("With random energy transfer", font_size=40).to_corner(LEFT).shift(UP * 1.5)

        self.play(Transform(script3, script4))
        self.wait()

        script5 = Tex("And 7 Energy units", font_size=40).to_corner(LEFT).shift(UP * 1.5)

        for _ in range(30):
            if _ == 14:
                self.play(FadeIn(script5), FadeOut(script3))
                new_S_1, new_S_2 = self.generate_subsystems(6, 7)
                self.update_labels_scene_one(System_one, System_two, new_S_1, new_S_2)
                self.wait()
            else:
                new_S_1, new_S_2 = self.generate_subsystems(6, 7)
                self.update_labels_scene_one(System_one, System_two, new_S_1, new_S_2)

        self.wait()

        script6 = Tex("System's microstate table:",
                      font_size=35).to_corner(RIGHT).shift(UP * 3).shift(LEFT * 3)

        self.play(FadeIn(script6), FadeOut(Title_Underline), FadeOut(Title))
        self.wait()

        Microstate_table = r"""
        \begin{tabular}{|p{2.3cm}|p{1.2cm}|p{2.5cm}|}
             \hline
             Integer pairs & $\Omega$ & Entropy $S/k_{b}$ \\
             \hline
             1+6 &  6 & 1.8 \\
             2+5 & 90 & 4.5 \\ 
             3+4 & 300 & 5.7 \\
             4+3 & 300 & 5.7 \\
             5+2 & 90 & 4.5 \\ 
             6+1 & 6 & 1.8 \\
            \hline   
        \end{tabular}

        """
        Mini_Microstate_table = Tex(Microstate_table).scale(0.7).to_corner(RIGHT).shift(UP * 1)

        self.play(Write(Mini_Microstate_table), run_time=1.5)

        self.wait()

        for _ in range(20):
            new_S_1, new_S_2 = self.generate_subsystems(6, 7)
            self.update_labels_scene_one(System_one, System_two, new_S_1, new_S_2)

        self.wait()
        Title3 = Tex("For a more complex simulation", font_size=42).to_corner(LEFT + UP)

        self.play(FadeOut(Mini_Microstate_table), FadeOut(System_one), FadeOut(System_two), FadeOut(script5),
                  FadeOut(script6), FadeIn(Title3, shift=DOWN), run_time=1)

        """
        2nd section of the Manim animations

        """

        # apply function for the random sequence changes for system_one and system_two

        s_1, s_2 = self.generate_subsystems(12, 12)

        subsystem_1 = self.create_subsystem_one(s_1, 0.8)
        subsystem_1.shift(LEFT * 5)

        subsystem_2 = self.create_subsystem_two(s_2, 0.8)
        subsystem_2.shift(LEFT * 5).shift(DOWN * 1.5)

        rect = Rectangle(height=3, width=10, stroke_color=RED, stroke_width=2)
        rect.move_to(LEFT * 0.63 + DOWN * 0.75)

        # Create the label
        label = Tex("Isolated System", color=WHITE, font_size=40)
        label.next_to(rect, UP, buff=0.2).shift(LEFT * 3.2)

        ## Create the legend
        Heated_particle = Circle(radius=0.125, stroke_width=1, stroke_color=WHITE).shift(UP * 1.5)
        Heated_particle.set_color(RED).set_opacity(1)
        Heated_particle_description = Tex("Hot: ", font_size=30).shift(UP * 1.5).shift(LEFT * 0.7)

        Cold_particle = Circle(radius=0.125, stroke_width=1, stroke_color=WHITE).shift(UP * 1)
        Cold_particle.set_color(BLUE_B).set_opacity(1)
        Cold_particle_description = Tex("Cold: ", font_size=30).shift(UP * 1).shift(LEFT * 0.7)

        ## Create the entropy level
        current_entropy = self.calculate_entropy(s_1, s_2)
        entropy_label = Tex(r"Entropy: {:.1f}".format(current_entropy), font_size=30)
        entropy_label.shift(RIGHT * 3).shift(UP * 2)

        Current_energy_1 = np.sum(s_1)
        Second_energy_1 = np.sum(s_2)
        system1_label = Tex(r"System 1 energy: {}".format(Current_energy_1), font_size=30)
        system2_label = Tex(r"System 2 energy: {}".format(Second_energy_1), font_size=30)

        system1_label.shift(RIGHT * 3).shift(UP * 1.5)
        system2_label.shift(RIGHT * 3).shift(UP * 1.0)

        self.play(FadeIn(subsystem_1), FadeIn(subsystem_2), FadeIn(rect),
                  FadeIn(label), FadeIn(system1_label),
                  FadeIn(system2_label), FadeIn(entropy_label),
                  FadeIn(Heated_particle_description), FadeIn(Cold_particle_description),
                  FadeIn(Heated_particle), FadeIn(Cold_particle), run_time=1.5)

        self.wait()

        # Generate a new configuration and animate the change
        for _ in range(36):
            new_s_1, new_s_2 = self.generate_subsystems(12, 12)
            s_1, s_2 = self.animate_configuration_change(s_1, s_2, subsystem_1, subsystem_2, new_s_1, new_s_2)

            heated_particles_1 = np.sum(s_1)
            heated_particles_2 = np.sum(s_2)
            entropy = self.calculate_entropy(s_1, s_2)
            self.update_labels(entropy, entropy_label, system1_label, system2_label, heated_particles_1,
                               heated_particles_2)

        self.wait()

        black_rect = Rectangle(fill_color=BLACK, fill_opacity=1, stroke_opacity=0, width=35, height=25)
        self.play(FadeIn(black_rect, run_time=1.5))
        self.wait()

    def create_subsystem_one(self, s1, spacing):
        subsystem_1 = VGroup()
        for index, state in enumerate(s1):
            circle = Circle(radius=0.25, stroke_width=1, stroke_color=WHITE)
            circle.set_color(RED if state == 1 else BLUE_B).set_opacity(1)
            circle.move_to(RIGHT * index * spacing)
            subsystem_1.add(circle)

        return subsystem_1

    def create_subsystem_two(self, s2, spacing):
        subsystem_2 = VGroup()
        for index, state in enumerate(s2):
            circle = Circle(radius=0.25, stroke_width=1, stroke_color=WHITE)
            circle.set_color(RED if state == 1 else BLUE_B).set_opacity(1)
            circle.move_to(RIGHT * index * spacing)
            subsystem_2.add(circle)

        return subsystem_2

    def generate_subsystems(self, length, total_ones):
        ones_positions = random.sample(range(2 * length), total_ones)
        s_1 = [0] * length
        s_2 = [0] * length

        for pos in ones_positions:
            if pos < length:
                s_1[pos] = 1
            else:
                s_2[pos - length] = 1

        return s_1, s_2

    def animate_configuration_change(self, s_1, s_2, subsystem_1, subsystem_2, new_s_1, new_s_2):
        animations = []
        for index in range(len(s_1)):
            if s_1[index] != new_s_1[index]:
                new_color = RED if new_s_1[index] == 1 else BLUE_B
                animations.append(subsystem_1[index].animate.set_color(new_color))

            if s_2[index] != new_s_2[index]:
                new_color = RED if new_s_2[index] == 1 else BLUE_B
                animations.append(subsystem_2[index].animate.set_color(new_color))

        self.play(*animations, run_time=0.4)
        return new_s_1, new_s_2

    def calculate_entropy(self, system1, system2):
        heated_particles1 = np.sum(system1)
        heated_particles2 = np.sum(system2)
        microstates = comb(len(system1), heated_particles1) * comb(len(system2), heated_particles2)
        entropy = np.log(microstates)
        return entropy

    def update_labels(self, entropy, entropy_label, system1_label, system2_label, heated_particles1,
                      heated_particles_2):
        """
        Heated_particles_1 is the number of particles that are red in system 1 list
        Heated_particles_2 is the number of particles that are red in system 2 list

        """
        entropy_label.become(Tex(r"Entropy: {:.2f}".format(entropy), font_size=30)
                             .shift(RIGHT * 3.2).shift(UP * 2))
        system1_label.become(Tex(r"System 1 energy: {}".format(heated_particles1), font_size=30)
                             .shift(RIGHT * 3).shift(UP * 1.5))
        system2_label.become(Tex(r"System 2 energy: {}".format(heated_particles_2), font_size=30)
                             .shift(RIGHT * 3).shift(UP * 1))

    def update_labels_scene_one(self, System_one, System_two, s1, s2):
        """
        Take the lists and make it become a string
        """
        string_1 = r"$s_{1}= $" + str(s1)
        string_2 = r"$s_{2}= $" + str(s2)
        System_one.become(Tex(string_1, font_size=40).to_corner(LEFT).shift(UP * 0.8))
        System_two.become(Tex(string_2, font_size=40).to_corner(LEFT))
        self.wait(0.4)

"""
PART 2, Scene 1: Cellular Automata Manim
Call this function on Pycharm's command promt: manim -p -qh Manimations.py GOL
"""

class GOL(MovingCameraScene):
    def construct(self):
        """
        First Manim Scene
        """
        ## Generate the intial grid for the ImageMobject
        generate_initial_grid = np.random.randint(0, 2, size=(250, 500))
        generate_multiplier = np.random.choice([0, 1], size=(250, 500), p=[0.83, 0.17])
        generate_initial = generate_multiplier * generate_initial_grid

        ## Get the grid running first before assembling it
        for _ in range(2):
            generate_initial = self.game_of_life(generate_initial)

        ## Apply lambda function to convert from 1s to 0s and its inverse
        convert_function = lambda x: 255 if x == 1 else 0
        conversion_function = np.vectorize(convert_function)
        inverse = lambda y: 1 if y == 255 else 0
        inverse_function = np.vectorize(inverse)

        ## Convert 1s and 0s into a 0 or 255 image for Manim
        initial_grid = conversion_function(generate_initial).astype(np.uint8)

        Title = Tex("This is the Game of life", font_size=45).to_corner(UP + LEFT)

        # Convert the NumPy array to an image
        self.play(FadeIn(Title, shift=DOWN))
        self.wait()

        height = 8
        width = 16

        grid = np.copy(initial_grid)

        epoch = 120
        grid_images_group = Group()

        ## Preprocess the grid first and create ImageMobjects
        GOL_grids = []
        for i in range(epoch):
            grid = inverse_function(grid)
            grid = self.game_of_life(grid)
            grid = conversion_function(grid)

            grid_image = ImageMobject(grid)
            grid_image.height = height
            grid_image.width = width
            grid_image.to_corner(LEFT).shift(LEFT * 1)
            grid_image.set_resampling_algorithm(RESAMPLING_ALGORITHMS["box"])

            GOL_grids.append(grid_image)

        ## Iterate the grid through the game of life rules
        for k in range(epoch):
            grid_images_group.add(GOL_grids[k])

            if k == 0:
                self.play(FadeIn(GOL_grids[0]))
            elif 1 <= k <= (epoch - 1):
                self.play(Transform(GOL_grids[k - 1], GOL_grids[k]), run_time=0.02)
                self.wait(0.13)

        self.wait()
        self.play(FadeOut(grid_images_group), FadeOut(Title))
        self.wait()

    def game_of_life(self, array):
        neighbor_vector = np.array([[1, 1, 1],
                                    [1, 0, 1],
                                    [1, 1, 1]], dtype=np.uint8)

        num_neighbors = signal.convolve2d(array, neighbor_vector,
                                          mode='same', boundary='wrap')

        next_state = np.logical_or(num_neighbors == 3,
                                   np.logical_and(num_neighbors == 2,
                                                  array)
                                   ).astype(np.uint8)
        array = next_state
        return array

"""
2nd Scene of Cellular automata : Introduces the rules of the game and the main ideas of my simulation
Call this function on Pycharm's command promt: manim -p -qh Manimations.py GameRules
"""

class GameRules(MovingCameraScene):
    def construct(self):

        Title = Tex("The Big idea:").to_corner(UP + LEFT)
        Title_Underline = Underline(Title, buff=0.15)

        Game_Rules = r"""
        \begin{minipage}{7cm}
        \begin{itemize}
            \item A live cell with fewer than two live neighbours dies.
            \item A live cell with two or three live neighbours lives on.
            \item A live cell with more than three live neighbours dies.
            \item A dead cell with exactly three live neighbours becomes a live cell.
        \end{itemize}
        \end{minipage}
        """

        subtitle = Tex("The rules", font_size=40).to_corner(LEFT).shift(UP * 2.2)

        GOL_rules = Tex(Game_Rules, font_size=30).to_corner(LEFT)

        self.play(FadeIn(Title, shift=DOWN), FadeIn(Title_Underline),
                  FadeIn(GOL_rules, shift=UP), Write(subtitle))
        self.wait(2)

        Game_of_life_code = '''import numpy as np
from scipy.ndimage import convolve

def game_of_life(array):
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]], 
                    dtype=np.uint8)

    neighbors=convolve(array, kernel, mode="constant")

    next_state = np.logical_or(neighbors == 3,
            np.logical_and(neighbors == 2,array)
            ).astype(np.uint8)

    array = next_state
    return array
    '''

        code = Code(code=Game_of_life_code, tab_width=4, background="rectangle",
                    language="Python", font="Monospace", background_stroke_width=0,
                    style="github-dark").to_corner(RIGHT).shift(RIGHT * 2.6).scale(0.60)

        self.play(FadeIn(code, shift=UP))
        self.wait(5)

        Title2 = Tex("How it works", font_size=50).to_corner(UP + LEFT)
        Title2_underline = Underline(Title2, buff=0.15)

        self.play(Transform(Title, Title2), Transform(Title_Underline, Title2_underline),
                  FadeOut(GOL_rules), FadeOut(subtitle))

        ## Create the grid
        self.create_grid(5, 5, 0.4, code)

        Title3 = Tex("Scaling it up", font_size=50).to_corner(UP + LEFT)
        self.play(FadeOut(Title), FadeOut(Title_Underline))
        self.play(FadeIn(Title3))
        self.wait()

        ## Play in the game of life code again using a function
        # Start with a random grid
        arr = np.random.randint(0, 2, (35, 70))
        generate_multiplier = np.random.choice([0, 1], size=(35, 70), p=[0.6, 0.4])
        grid = arr * generate_multiplier

        # Create the grid of rectangles
        rect_group = self.create_square_grid(grid, 0.2)
        self.play(FadeIn(rect_group), FadeOut(Title3))

        # Run the Game of Life for a few steps
        for _ in range(70):
            grid = self.game_of_life(grid)
            rect_group = self.update_colors(rect_group, grid)
            self.wait(0.15)

        self.wait()
        Black_rectangle = Rectangle(fill_color=BLACK, fill_opacity=1, stroke_opacity=0, width=20, height=25)
        self.play(FadeIn(Black_rectangle))
        self.wait()

    def create_grid(self, rows, columns, size, code_mobject):

        no_of_rows = rows
        no_of_columns = columns

        square_size = size

        grid_group = VGroup()
        kernel_group = VGroup()

        numbers_array = np.random.randint(0, 2, size=(no_of_rows, no_of_columns))

        # Iterate through each row and column to create the grid
        for row in range(no_of_rows):
            for column in range(no_of_columns):
                # Create a square
                square = Square(side_length=square_size)

                # Position the square based on its row and column
                square.shift((column - no_of_columns // 2) * square_size * RIGHT)
                square.shift((row - no_of_rows // 2) * square_size * UP)

                # Get the number from the NumPy array
                number = numbers_array[row, column]

                # Create a Tex object for the number
                number_tex = Tex(str(number), font_size=25)

                # Position the number at the center of the square
                number_tex.move_to(square.get_center())

                # Add the square and number to the grid_group
                grid_group.add(square)
                grid_group.add(number_tex)

        kernel_group = VGroup()
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.uint8)

        ## Iterate through the grid to create a kernel
        for kernel_row in range(3):
            for kernel_column in range(3):
                ## Create a square
                kernel_square = Square(side_length=square_size)

                kernel_square.shift((kernel_column - 3 // 2) * square_size * RIGHT)
                kernel_square.shift((kernel_row - 3 // 2) * square_size * UP)

                kern = kernel[kernel_row, kernel_column]

                kern_tex = Tex(str(kern), font_size=25)

                kern_tex.move_to(kernel_square.get_center())

                kernel_group.add(kernel_square)
                kernel_group.add(kern_tex)
        # Create the new yellow kernel
        colored_kernel = VGroup()

        # Create 8 yellow squares and 1 transparent square for the kernel
        kernel_colors = [YELLOW] * 9
        for i in range(9):
            if i == 4:
                Kernel_square = Square(side_length=square_size, fill_color=kernel_colors[i], fill_opacity=0)
            else:
                Kernel_square = Square(side_length=square_size, fill_color=kernel_colors[i], fill_opacity=0.5)
            Kernel_square.shift(((i % 3) - 1) * square_size * RIGHT)
            Kernel_square.shift(((i // 3) - 1) * square_size * UP)
            colored_kernel.add(Kernel_square)


        grid_group.to_corner(LEFT).shift(DOWN * 1)
        kernel_group.to_corner(LEFT + UP).shift(DOWN * 1)
        colored_kernel.to_corner(LEFT + UP).shift(DOWN * 1)

        ## Get the Brace Mobject
        array_description = BraceLabel(grid_group, "Array", brace_direction=DOWN, font_size=30)
        kernel_description = BraceLabel(kernel_group, "Kernel", brace_direction=DOWN, font_size=30)

        self.play(FadeIn(grid_group), FadeIn(kernel_group),
                  Write(array_description), Write(kernel_description), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(array_description), FadeOut(kernel_description))
        self.play(Transform(kernel_group, colored_kernel))
        self.wait()

        Right_arrow = Tex(r"$\Rightarrow$", font_size=50)
        Right_arrow.next_to(grid_group, RIGHT, buff=0.5)

        # Create the result grid
        result_group, final_result = self.convolve_result(numbers_array, square_size)
        result_group.next_to(Right_arrow, RIGHT, buff=0.5)

        self.play(FadeIn(Right_arrow), run_time=0.7)
        self.move_kernel(kernel_group, grid_group, no_of_rows, no_of_columns, square_size, result_group, code_mobject
                         , Right_arrow, final_result)
        self.wait()

    def move_kernel(self, kernel_group, grid_group, no_of_rows, no_of_columns, square_size, result_group, code_mobject
                    , Right_arrow, final_group):
        ## Set the final_group
        final_group.to_corner(LEFT).shift(DOWN * 1.5 + RIGHT * 1.75)

        # Initially, make all squares and their numbers in the result grid invisible
        rect = self.highlight_code_line(code_mobject, 9)  # Assuming the convolve operation is at line 9
        for idx, mobject in enumerate(result_group):

            if idx % 2 == 0:  # If it's a square
                mobject.set_stroke(width=3, color=WHITE)
                mobject.set_fill(opacity=0)  # Ensure the square is transparent

            else:  # If it's a number
                mobject.set_opacity(1)

        for i in range(no_of_rows * no_of_columns):
            target_square = grid_group[2 * i].get_center()
            shift_vector = target_square - kernel_group[-1].get_center() + (UP * square_size + RIGHT * square_size)

            # play the run lamda function

            running = lambda i: 1 if 0 <= i <= 4 else 0.3

            self.play(kernel_group.animate.shift(shift_vector), run_time=running(i))

            # Fade in the square and its number
            self.play(FadeIn(result_group[2 * i]), FadeIn(result_group[2 * i + 1]),
                      run_time=running(i))  # Square and number

        self.play(Uncreate(rect), FadeOut(kernel_group), run_time=1)
        self.wait()
        self.play(grid_group.animate.shift(UP * 2), result_group.animate.shift(UP * 2), FadeOut(Right_arrow))
        self.wait()

        for index, mobject in enumerate(final_group):
            if index % 2 == 0:
                mobject.set_stroke(width=3, color=WHITE)
                mobject.set_fill(opacity=0)
            else:
                mobject.set_opacity(1)

        rectangle = self.highlight_code_line(code_mobject, 11, kernel=False)
        for k in range(no_of_rows * no_of_columns):
            arrow1, arrow2 = self.arrows_compare(grid_group[2 * k + 1], result_group[2 * k + 1], final_group[2 * k + 1])
            run = lambda k: 1 if 0 <= k <= 3 else 0.3

            # play the animations
            self.play(Create(arrow1), Create(arrow2), FadeIn(final_group[2 * k]), FadeIn(final_group[2 * k + 1]),
                      run_time=run(k))
            self.play(FadeOut(arrow1), FadeOut(arrow2), run_time=run(k) / 2)

        self.wait(2)
        ## Label the grids
        final_group_label = BraceLabel(final_group, "Array", brace_direction=LEFT, font_size=30)
        self.play(FadeIn(final_group_label))
        self.wait(2.5)
        self.play(FadeOut(grid_group), FadeOut(final_group), FadeOut(result_group), FadeOut(final_group_label),
                  Uncreate(rectangle))
        self.play(FadeOut(code_mobject))
        self.wait()

    def convolve_result(self, array, square_size):
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.uint8)
        neighbours = convolve(array, kernel, mode="constant")

        next_state = np.logical_or(neighbours == 3, np.logical_and(neighbours == 2, array)).astype(np.uint8)

        Result = VGroup()

        no_of_rows = neighbours.shape[0]
        no_of_columns = neighbours.shape[1]

        # Iterate through each row and column to create the grid of neighbours
        for row in range(no_of_rows):
            for column in range(no_of_columns):
                # Create a square with transparent fill and visible borders
                square = Square(side_length=square_size, fill_opacity=0, stroke_width=0, stroke_color=WHITE)

                # Position the square based on its row and column
                square.shift((column - no_of_columns // 2) * square_size * RIGHT)
                square.shift((row - no_of_rows // 2) * square_size * UP)

                # Get the number from the NumPy array
                number = neighbours[row, column]

                # Create a Tex object for the number
                number_tex = Tex(str(number), font_size=25)

                # Position the number at the center of the square
                number_tex.move_to(square.get_center())

                # Add the square and number to the grid_group
                Result.add(square)
                Result.add(number_tex)

        Final_result = VGroup()
        ## Iterate the next state of the game of life
        for rows in range(next_state.shape[0]):
            for columns in range(next_state.shape[1]):
                square = Square(side_length=square_size, fill_opacity=0, stroke_width=0, stroke_color=WHITE)

                square.shift((columns - next_state.shape[1] // 2) * square_size * RIGHT)
                square.shift((rows - next_state.shape[0] // 2) * square_size * UP)

                numbers = next_state[rows, columns]

                numbers_tex = Tex(str(numbers), font_size=25)

                numbers_tex.move_to(square.get_center())

                Final_result.add(square)
                Final_result.add(numbers_tex)

        return Result, Final_result

    def highlight_code_line(self, code_mobject, line_number, kernel=True):
        # Highlight the line
        if kernel:
            rect = SurroundingRectangle(code_mobject.code[line_number], color=RED, buff=0.05).shift(DOWN * 0.12)
            self.play(Create(rect), run_time=0.5)
        else:
            rect = SurroundingRectangle(code_mobject.code[line_number], color=RED, buff=0.2).shift(DOWN * 0.35)
            self.play(Create(rect), run_time=0.5)

        return rect

    def arrows_compare(self, element1, element2, final_element):
        arrow1 = Arrow(start=element1.get_center(), end=final_element.get_center(), color=RED, buff=0)
        arrow2 = Arrow(start=element2.get_center(), end=final_element.get_center(), color=RED, buff=0)

        return arrow1, arrow2

    def game_of_life(self, grid):
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=np.uint8)

        num_neighbors = signal.convolve2d(grid, kernel, mode='same', boundary='wrap')

        next_state = np.logical_or(num_neighbors == 3, np.logical_and(num_neighbors == 2, grid)).astype(np.uint8)

        return next_state

    def create_square_grid(self, grid, size):
        no_of_rows = grid.shape[0]
        no_of_columns = grid.shape[1]

        rect_group = VGroup()

        # Iterate through each row and column to create the grid
        for row in range(no_of_rows):
            for column in range(no_of_columns):
                # Create a rectangle
                rect = Rectangle(height=size, width=size, stroke_width=0.1)

                # Position the rectangle based on its row and column
                rect.shift((column - no_of_columns // 2) * size * RIGHT)
                rect.shift((row - no_of_rows // 2) * size * UP)

                # Color the rectangle based on the value in the grid
                if grid[row, column]==1:
                    cl=WHITE
                else:
                    cl=BLACK

                # noinspection PyArgumentList
                rect.set_fill(color=cl, opacity=1.0)
                # Add the rectangle to the group
                # inspection PyArgumentList
                rect_group.add(rect)

        return rect_group

    def update_colors(self, rect_group, grid):
        no_of_rows = grid.shape[0]
        no_of_columns = grid.shape[1]

        # Iterate through each rectangle in the group and update its color
        for i, rect in enumerate(rect_group):
            # Calculate the row and column of this rectangle
            row = i // no_of_columns
            column = i % no_of_columns

            # Update the color of the rectangle
            rect.set_fill(color=WHITE if grid[row, column] else BLACK, opacity=1)

        return rect_group


"""
Scene 3: Manim animations, Early ideas of cellular automata 
The scene is version 1 of my Stochastic cellular automata game 
Call the function:  manim -p -qh Manimations.py Automata
"""

class Automata(Scene):
    def construct(self):
        Title = Tex("Early ideas").to_corner(LEFT + UP)

        Automata_rules = r"""
        \begin{minipage}{8cm}
        \begin{itemize}
            \item A cell can only be 1 or 0.
            \item The number of 1s within the grid cannot change.
            \item An occupied cell can move in a random direction to its Moore neighbourhood if unoccupied.
        \end{itemize}
        \end{minipage}
    """

        subtitle = Tex("The rules", font_size=40).to_corner(LEFT).shift(UP * 2.3)
        Rules = Tex(Automata_rules, font_size=33).to_corner(LEFT)

        self.play(FadeIn(Title, shift=DOWN), FadeIn(subtitle, shift=UP), Write(Rules))
        self.wait(2)

        subtitle2 = Tex("Neighbours").to_corner(RIGHT + UP).shift(LEFT * 2)
        subtitle3 = Tex("Possible directions").to_corner(RIGHT + UP).shift(LEFT * 1.8)
        self.play(FadeIn(subtitle2))

        moore_group, von_neumann_group = self.neighbour_mobject(0.5)
        moore_group.to_corner(RIGHT).shift(UP * 1.5 + LEFT * 2.7)
        von_neumann_group.to_corner(RIGHT).shift(DOWN * 1 + LEFT * 2.7)

        Brace_desc = BraceLabel(moore_group, "Moore", font_size=30, brace_direction=DOWN, buff=0.1)
        Neumann_brace = BraceLabel(von_neumann_group, "Neumann", font_size=30, brace_direction=DOWN, buff=0.1)

        rect = Rectangle(color=RED, height=1.5, width=8.0, stroke_width=2).to_corner(LEFT).shift(DOWN * 1 + LEFT * 0.2)

        self.play(FadeIn(moore_group), FadeIn(von_neumann_group), FadeIn(Brace_desc), FadeIn(Neumann_brace))
        self.wait(5)

        self.play(FadeOut(von_neumann_group), FadeOut(Brace_desc), FadeOut(Neumann_brace))
        self.wait(2)
        self.play(moore_group.animate.shift(DOWN * 1.5))
        self.play(moore_group.animate.scale(2))

        ## Create arrows first
        arrows = self.arrows_probability(moore_group)
        Title2 = Tex("Simulation at scale").to_corner(UP + LEFT)
        ## Create the objects and fade into Manim Scene
        self.play(Create(rect), Transform(subtitle2, subtitle3))
        self.play(FadeIn(arrows))
        self.wait(5)
        self.play(FadeOut(subtitle2), Uncreate(rect), FadeOut(arrows), FadeOut(moore_group))
        self.play(Transform(Title, Title2), Rules.animate.to_corner(RIGHT),
                  subtitle.animate.shift(RIGHT * 7.0 + UP * 1))
        self.play(Rules.animate.shift(UP * 1), subtitle.animate.scale(1.2))
        ## Now play the function
        self.Automata_loop(50, 0.12, 10)

    def neighbour_mobject(self, square_size):
        moore_group = VGroup()
        kernel_colors = [YELLOW] * 9
        for i in range(9):
            if i == 4:
                Kernel_square = Square(side_length=square_size, fill_color=kernel_colors[i], fill_opacity=0)
            else:
                Kernel_square = Square(side_length=square_size, fill_color=kernel_colors[i], fill_opacity=0.5)
            Kernel_square.shift(((i % 3) - 1) * square_size * RIGHT)
            Kernel_square.shift(((i // 3) - 1) * square_size * UP)
            moore_group.add(Kernel_square)

        ## Now define the von_neumann_group

        von_neumann_group = VGroup()
        group_colors = [TEAL_A] * 9

        for j in range(9):
            if j % 2 == 0:
                squares = Square(side_length=square_size, fill_color=group_colors[j], fill_opacity=0)
            else:
                squares = Square(side_length=square_size, fill_color=group_colors[j], fill_opacity=0.5)

            squares.shift(((j % 3) - 1) * square_size * RIGHT)
            squares.shift(((j // 3) - 1) * square_size * UP)
            von_neumann_group.add(squares)

        return moore_group, von_neumann_group

    def arrows_probability(self, mobject):
        Arrows = VGroup()
        center_square = mobject[4]
        for idx, square in enumerate(mobject):
            if idx != 4:
                arrow = self.arrow(center_square, square)
                Arrows.add(arrow)

        return Arrows

    def arrow(self, start_square, end_square):
        start = start_square.get_center()
        end = end_square.get_center()

        return Arrow(start=start, end=end, color=GREY_A)

    def create_large_grid(self, grid: np.ndarray, square_size=0.1):
        grid_length = grid.shape[0]
        grid_width = grid.shape[1]

        grid_group = VGroup()

        for rows in range(grid_length):
            for columns in range(grid_width):
                ## Create the rectangles necessary
                Rect = Rectangle(height=square_size, width=square_size, stroke_width=0.05)

                Rect.shift((columns - grid_width // 2) * square_size * RIGHT)
                Rect.shift((rows - grid_length // 2) * square_size * UP)

                if grid[rows, columns] == 1:
                    cl = RED_E
                else:
                    cl = BLUE_A

                # noinspection PyArgumentList
                Rect.set_fill(color=cl, opacity=1.0)
                # Add the rectangle to the group
                # inspection PyArgumentList
                grid_group.add(Rect)

        return grid_group

    def update_colors(self, grid_group, grid: np.ndarray):
        no_of_rows = grid.shape[0]
        no_of_columns = grid.shape[1]

        # Iterate through each rectangle in the group and update its color
        for index, Rectangles in enumerate(grid_group):
            # Calculate the row and column of this rectangle
            row = index // no_of_columns
            column = index % no_of_columns

            # Update the color of the rectangle
            Rectangles.set_fill(color=RED_E if grid[row, column] else BLUE_A, opacity=1)

        return grid_group

    ## Automata has attribute automata_function so that it can run early CA grid structures.
    def automata_function(self, grid, heat_transfer_probability=1):
        black_cells = np.where(grid[1:-1, 1:-1] == 1)
        indices = np.arange(len(black_cells[0]))
        np.random.shuffle(indices)
        black_cells = (black_cells[0][indices], black_cells[1][indices])
        direction_vector = np.array([[0, -1], [-1, 0], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]])

        for i in range(len(black_cells[0])):
            x, y = black_cells[0][i] + 1, black_cells[1][i] + 1
            if np.random.rand() < heat_transfer_probability:
                neighbors = np.array(
                    [grid[x][y - 1], grid[x - 1][y], grid[x + 1][y], grid[x][y + 1], grid[x - 1][y - 1],
                     grid[x + 1][y - 1],
                     grid[x + 1][y + 1], grid[x - 1][y + 1]])
                if np.all(neighbors == 1) == True:
                    pass
                else:
                    boolean_dir_index = (neighbors == 0)
                    valid_directions = direction_vector[boolean_dir_index]
                    valid_directions_flat = valid_directions.reshape(-1, 2)
                    possible_directions = valid_directions_flat[np.random.choice(valid_directions_flat.shape[0])]
                    grid[x + possible_directions[0]][y + possible_directions[1]] = 1
                    grid[x][y] = 0
        return grid

    def initialize_grid(self, length, choice="circle"):
        grid = np.pad(np.zeros((length, length)), pad_width=1, mode='constant', constant_values=1)
        if choice == "circle":
            center = ((length / 2), (length / 2))
            radius = int(math.sqrt(0.1 * length ** 2 / math.pi))
            x, y = np.meshgrid(np.linspace(0, length + 2, length + 2), np.linspace(0, length + 2, length + 2))
            distance = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
            grid[distance <= radius] = 1
        elif choice == "ellipse":
            center = (length // 2, length // 2)
            x, y = np.meshgrid(np.linspace(0, length + 2, length + 2), np.linspace(0, length + 2, length + 2))
            a = 0.13 * length  # x-radius
            b = 0.09 * length  # y-radius
            ellipse = (x - center[0]) ** 2 / a ** 2 + (y - center[1]) ** 2 / b ** 2
            grid[ellipse <= 1] = 1
        else:
            print("Invalid choice")
            sys.exit()

        test_grid = np.copy(grid)
        return grid, test_grid

    def Automata_loop(self, length, square_size, epochs):
        Grids = VGroup()
        length = length
        grid, initial_grid = self.initialize_grid(length, choice="circle")
        grid_object = self.create_large_grid(grid[1:-1, 1:-1], square_size=square_size).to_corner(LEFT)

        for k in range(epochs):
            grid = self.automata_function(grid, heat_transfer_probability=1)
            grid_object = self.update_colors(grid_object, grid[1:-1, 1:-1]).to_corner(LEFT)
            if k % 2 == 0:
                Grids.add(grid_object.copy())

        ## Play loop
        for i in range(len(Grids)):
            loop = lambda i: 1.5 if i == 0 else 0.1
            if i == 0:
                self.play(FadeIn(Grids[0]), run_time=loop(i))
                self.wait()
            else:
                self.play(Transform(Grids[i - 1], Grids[i]), run_time=loop(i))

        self.wait(3)
        Black_rectangle = Rectangle(color=BLACK, height=15, width=20)
        self.play(FadeIn(Black_rectangle))
        self.wait()


"""
Manim Scene 4 : Evolution of the ideas of cellular Automata simulation, more complex simulation 
Tell the boltzmann factors and the move probability concept. 
call the function:  manim -p -qh Manimations.py Automata_V2
"""

class Automata_V2(Scene):
    def construct(self):
        Title = Tex("Extending the idea and rules").to_corner(UP + LEFT)
        Title_Underline = Underline(Title, buff=0.1)

        Rule_space = r"""
    \begin{minipage}{7.5cm}
    \begin{itemize}
        \item The grid can only contain integers of the vector space $\mathbb{Z}^{2}$.
        \item The sum of the integers cannot change over time.
        \item An non-zero-cell can transfer 1 energy unit to its neighbour according to its boltzmann factors
    \end{itemize}
    \end{minipage}
    """
        Rules = Tex(Rule_space, font_size=35).to_corner(LEFT).shift(UP * 0)
        self.play(FadeIn(Title, shift=DOWN), FadeIn(Title_Underline), Write(Rules))
        self.wait(2)

        ## Get the neighbour mobject and arrow mobject
        Number_list_int = [1, 3, 2, 6, 7, 8, 5, 0, 4]
        Number_list_two = [1, 3, 2, 6, 6, 8, 5, 1, 4]
        Number_list_three = [1, 3, 3, 6, 6, 8, 5, 0, 4]
        Number_list_four = [1, 3, 2, 7, 6, 8, 5, 0, 4]
        LIST = [Number_list_int, Number_list_two, Number_list_three, Number_list_four]
        LIST = np.array(LIST)
        Neighbour = self.moore_neighbours(0.85, LIST, 1, to_branches=False).to_corner(RIGHT).shift(LEFT * 1.5 + UP * 1)
        Arrow_mobjects = self.arrows_probability(Neighbour)

        Side_title = Tex("Example").to_corner(RIGHT + UP).shift(LEFT * 2)
        self.wait(5)

        ## Create the legends
        Legend = VGroup()
        Selected_cell = Tex("Selected", font_size=20).next_to(Neighbour, DOWN)
        Square_one = Square(side_length=0.4, fill_color=BLUE_C, fill_opacity=0.8).next_to(Selected_cell)
        # Create the 2nd legend
        Legends = self.create_legends(0.4, Neighbour, 25)

        ## Get the boltzmann factors into the picture.
        Title2 = Tex("The boltzmann factors").to_corner(UP + LEFT)
        Title2_Underline = Underline(Title2, buff=0.1)
        Later_rule = r"""
    \begin{minipage}{7.5cm}
    \begin{itemize}
        \item An non-zero-cell can transfer 1 energy unit to its neighbour according to its boltzmann factors
    \end{itemize}
    \end{minipage}
    """

        Latter_rule = Tex(Later_rule, font_size=30).to_corner(LEFT).shift(UP * 2)
        Boltzmann_equation = MathTex(r"\frac{p_{i}}{p_{j}} = \exp\left(\frac{\epsilon_{j}-\epsilon_{i}}{kT}\right)",
                                     font_size=35).to_corner(LEFT).shift(UP * 0.5)
        self.play(Transform(Title, Title2), Transform(Title_Underline, Title2_Underline), Transform(Rules, Latter_rule))
        self.play(Write(Boltzmann_equation))
        self.wait(3)

        ## Change the Later rules
        Title3 = Tex("In the context of the simulation", font_size=40).to_corner(UP + LEFT)
        self.play(FadeOut(Title_Underline), FadeOut(Title), FadeIn(Title3, shift=DOWN), Uncreate(Rules))

        Eq = MathTex(r"K_{j} = \exp\left(\frac{\Pi-\epsilon_{j}}{T}\right)", font_size=35).to_corner(LEFT).shift(
            UP * 2.0)
        description = Tex("*$\Pi$ is the maximum integer value in the simulation", font_size=30).move_to(ORIGIN).shift(
            DOWN * 3)
        self.play(Boltzmann_equation.animate.shift(UP * 1.5))
        self.play(Transform(Boltzmann_equation, Eq), Write(description))

        self.wait(2)

        ## Perform the calculation in this section
        Title4 = Tex("Calculating the probabilities", font_size=40).to_corner(UP + LEFT)
        description_two = Tex("*In this case 8, is the maximum and T is 1", font_size=30).move_to(ORIGIN).shift(
            DOWN * 3)
        self.play(Transform(Title3, Title4), Create(Neighbour), FadeIn(Side_title, shift=DOWN), Create(Legends))
        self.play(Create(Arrow_mobjects))
        self.play(Transform(description, description_two))
        self.wait(3)

        ## Run the self.complex_animation() function
        # self.complex_animation(Neighbour)
        Calculations = Tex("Calculations", font_size=40).to_corner(LEFT).shift(UP * 1).set_color(GREEN_A)
        self.play(FadeIn(Calculations))
        Results, Normalized_probs = self.complex_animation(Neighbour)
        self.wait(3)
        Calcs = Tex("Partision function", font_size=40).to_corner(LEFT).shift(UP * 1).set_color(GREEN_A)
        Brace_label = BraceLabel(Results, r"Total: \sim4712", buff=0.1, font_size=30).shift(UP * 1.5)
        prob_description = BraceLabel(Normalized_probs, "Probabilities", buff=0.1, font_size=28)
        self.play(Results.animate.shift(UP * 1.5))
        self.play(Write(Brace_label))
        self.wait(3)
        self.play(Uncreate(Brace_label), Transform(Calculations, Calcs), FadeOut(Boltzmann_equation))

        ## Play the animation for a new probability
        Probs = MathTex(r"p_{j} = \exp\left(\frac{\Pi-\epsilon_{j}}{T}\right) / \sum_{j=1}^{\kappa} K_{j}  ",
                        font_size=35).to_corner(LEFT).shift(UP * 2.0)
        Probs_transformation = MathTex(r"p_{j} = \exp\left(\frac{\Pi-\epsilon_{j}}{T}\right) / 4712",
                                       font_size=35).to_corner(LEFT).shift(UP * 2)
        self.play(Create(Normalized_probs), FadeIn(Probs, shift=DOWN))
        self.play(FadeIn(prob_description, shift=UP))
        self.wait(2)
        self.play(TransformMatchingShapes(Probs, Probs_transformation))
        self.wait(3)

        ## Animate the square mobject and create arrows connected to 3 different square mobjects with changed value highlighted.
        # Change the title, remove the Side_title, remove the Results, move the Normalized_probs and its Brace up.
        New_Title = Tex("What this means").to_corner(LEFT + UP)
        New_Title_Underline = Underline(New_Title, buff=0.1)
        self.play(FadeOut(Side_title), Uncreate(Results), FadeOut(Title3), FadeOut(Calculations), FadeOut(description),
                  FadeOut(Probs_transformation), FadeOut(Legends))
        self.play(Create(New_Title), Create(New_Title_Underline), Uncreate(Normalized_probs),
                  Uncreate(prob_description), Uncreate(Arrow_mobjects))
        self.wait()

        self.play(Neighbour.animate.to_corner(LEFT))
        self.play(Neighbour.animate.shift(DOWN * 1 + RIGHT * 1.5))
        self.wait(2)

        ## Create a list of lists
        Branches, Directions, Braces = self.create_arrows_and_squares(Neighbour, LIST)
        New_legend = self.create_legends(0.4, Neighbour, 30, for_evolution=True).to_corner(UP + RIGHT)
        self.play(FadeIn(Branches), FadeIn(Directions), Create(New_legend))
        self.play(FadeIn(Braces))
        self.wait(5)
        self.play(FadeOut(New_Title_Underline), FadeOut(Branches), FadeOut(Directions), FadeOut(Braces),
                  FadeOut(New_legend), FadeOut(Neighbour))

        ## To do, Modify the self.create_arrows_and_squares function by adding BraceLabel Mobject and make the Simulation Scene with Code.
        Transition_title = Tex("Scaling the simulation").to_corner(LEFT + UP)
        self.play(Transform(New_Title, Transition_title))
        self.wait()
        Legend = self.create_legends(0.35, None, 25, for_evolution=None)
        SIDE_TITLE = Tex("Energy level", font_size=40).to_corner(UP).shift(RIGHT * 3)
        En_level = Legend.next_to(SIDE_TITLE, DOWN)
        self.play(Create(En_level), FadeIn(SIDE_TITLE))
        self.wait(2)

        self.Automata_loop(50, "circle" , 0.12, 60)

    def create_legends(self, square_size, Math_Object: Mobject, Font_size, for_evolution=False):
        global Legend
        if for_evolution == False:
            ## Create the legends
            Legend = VGroup()
            Selected_cell = Tex("Selected :", font_size=Font_size).next_to(Math_Object, DOWN * 1.5)
            Square_one = Square(side_length=square_size, fill_color=BLUE_C, fill_opacity=0.8).next_to(Selected_cell)
            # Create the 2nd legend
            Unoccupied_cell = Tex("Available :", font_size=Font_size).next_to(Selected_cell, DOWN * 1.5).shift(
                LEFT * 0.07)
            Square_two = Square(side_length=square_size, fill_color=WHITE, fill_opacity=0.8).next_to(Unoccupied_cell)
            ## Create the 3rd legend
            Full_cell = Tex("Unavailable :", font_size=Font_size).next_to(Unoccupied_cell, DOWN * 1.5).shift(
                LEFT * 0.12)
            Square_three = Square(side_length=square_size, fill_color=RED_C, fill_opacity=0.8).next_to(Full_cell)

            Legend.add(Selected_cell, Square_one, Unoccupied_cell, Square_two, Full_cell, Square_three)

        elif for_evolution == True:
            Legend = VGroup()
            Selected_cell = Tex("Selected :", font_size=Font_size).next_to(Math_Object, DOWN * 1.5)
            Square_one = Square(side_length=square_size, fill_color=BLUE_C, fill_opacity=0.8).next_to(Selected_cell)
            # Create the 2nd legend
            Unoccupied_cell = Tex("Available :", font_size=Font_size).next_to(Selected_cell, DOWN * 1.5).shift(
                LEFT * 0.07)
            Square_two = Square(side_length=square_size, fill_color=WHITE, fill_opacity=0.8).next_to(Unoccupied_cell)
            ## Create the 3rd legend
            Full_cell = Tex("Unavailable :", font_size=Font_size).next_to(Unoccupied_cell, DOWN * 1.5).shift(
                LEFT * 0.12)
            Square_three = Square(side_length=square_size, fill_color=RED_C, fill_opacity=0.8).next_to(Full_cell).shift(
                LEFT * 0.07)

            ## Create the 4th Legend
            Changed_cell = Tex("Changed :", font_size=Font_size).next_to(Full_cell, DOWN * 1.5).shift(LEFT * 0)
            Square_four = Square(side_length=square_size, fill_color=GREEN_C, fill_opacity=0.8).next_to(
                Changed_cell).shift(RIGHT * 0.140)

            Legend.add(Selected_cell, Square_one, Unoccupied_cell, Square_two, Full_cell, Square_three, Changed_cell,
                       Square_four)

        elif for_evolution == None and Math_Object == None:
            Legend = VGroup()
            numbers = [8, 7, 6, 5, 4, 3, 2, 1, 0]
            coloring = [BLUE_C, TEAL_B, GREEN_A, YELLOW_A, GOLD_A, ORANGE, RED_C, RED_E, MAROON_E]
            for k in range(len(numbers)):
                if k == 0:
                    selected_cell = Tex(str(numbers[k]) + " :", font_size=Font_size)
                    squares = Square(side_length=square_size, fill_color=coloring[k], fill_opacity=0.9,
                                     stroke_width=1).next_to(selected_cell)
                    Legend.add(selected_cell, squares)
                else:
                    Selected_cell = Tex(str(numbers[k]) + " :", font_size=Font_size).next_to(Legend[2 * k - 2],
                                                                                             DOWN * 1.5)
                    Squares = Square(side_length=square_size, fill_color=coloring[k], fill_opacity=0.9,
                                     stroke_width=1).next_to(Selected_cell)
                    Legend.add(Selected_cell, Squares)

        return Legend

    def moore_neighbours(self, square_size: float, Number_lists: np.ndarray, list_argument: int, to_branches=False):
        if to_branches == False:
            Neighbour = VGroup()
            kernel_colors = [WHITE] * 9

            for j in range(len(kernel_colors)):

                if j == 4:
                    Kernel_square = Square(side_length=square_size, fill_color=BLUE_C, fill_opacity=0.8)
                elif j == 5:
                    Kernel_square = Square(side_length=square_size, fill_color=RED_C, fill_opacity=0.8)
                else:
                    Kernel_square = Square(side_length=square_size, fill_color=kernel_colors[j], fill_opacity=0.8)

                Kernel_square.shift(((j % 3) - 1) * square_size * RIGHT)
                Kernel_square.shift(((j // 3) - 1) * square_size * UP)

                number = Tex(str(Number_lists[0, j]), font_size=35).set_color(BLACK)
                number.move_to(Kernel_square.get_center())

                Neighbour.add(Kernel_square)
                Neighbour.add(number)

            return Neighbour

        elif to_branches == True:
            Branches = VGroup()
            kernel_colors = [WHITE] * 9
            reference_list = Number_lists[0, :]
            for j in range(len(kernel_colors)):
                value = reference_list[j] == Number_lists[list_argument, j]
                if value == False:
                    Kernel_square = Square(side_length=0.75 * square_size, fill_color=GREEN_C, fill_opacity=0.8,
                                           stroke_width=2)
                elif j == 5:
                    Kernel_square = Square(side_length=0.75 * square_size, fill_color=RED_C, fill_opacity=0.8,
                                           stroke_width=2)
                else:
                    Kernel_square = Square(side_length=0.75 * square_size, fill_color=kernel_colors[j],
                                           fill_opacity=0.8, stroke_width=2)

                Kernel_square.shift(((j % 3) - 1) * (0.75 * square_size) * RIGHT)
                Kernel_square.shift(((j // 3) - 1) * (0.75 * square_size) * UP)

                number = Tex(str(Number_lists[list_argument, j]), font_size=35).set_color(BLACK)
                number.move_to(Kernel_square.get_center())

                Branches.add(Kernel_square)
                Branches.add(number)

            return Branches

    def arrows_probability(self, mobject):
        Arrows = VGroup()
        center_square = mobject[8]
        for idx, square in enumerate(mobject):
            if idx != 8:
                arrow = self.arrow(center_square, square)
                Arrows.add(arrow)

        return Arrows

    def arrow(self, start_square, end_square):
        start = start_square.get_center()
        end = end_square.get_center()

        return Arrow(start=start, end=end, color=GREEN_E)

    def complex_animation(self, square_mobjects):
        Results = VGroup()  ## The initial expression for the results group
        Results_two = VGroup()  ## The latter results when the partition function is applied.
        Total = math.exp(7) + math.exp(5) + math.exp(6) + math.exp(2) + 0 + math.exp(3) + math.exp(8) + math.exp(4)
        scale_factor = 1.3
        Number_list = ["1", "3", "2", "6", "8", "5", "0", "4"]
        for j in range(len(Number_list)):
            value = np.exp(8 - int(Number_list[j]))
            Calc = MathTex(f"K_{{{Number_list[j]}}} = ", font_size=35).to_corner(LEFT).shift(UP * 0.0)
            if j == 4:
                Result = MathTex(r"e^{-\infty}", font_size=35).next_to(Calc).shift(UP * 0.1)
                Result_two = MathTex("0", font_size=25)
            else:
                Result = MathTex(f"e^{{\\frac{{8-{Number_list[j]}}}{{1}}}}", font_size=35).next_to(Calc).shift(UP * 0.1)
                value = math.exp(8 - int(Number_list[j])) / Total
                Result_two = MathTex(f"{value:.4f}", font_size=25)

                ## Because of the way the arrow objects are created you need to multiply it by 2 to ensure correct indexing
            running_time = lambda j: 1 if 0 <= j <= 2 else 0.3
            if j == 0:
                self.play(Write(Calc), Write(Result), square_mobjects[9].animate.scale(scale_factor),
                          square_mobjects[j + (j + 1)].animate.scale(scale_factor), run_time=running_time(j))

                self.wait(running_time(j))

                self.play(Uncreate(Calc), Result.animate.shift(DOWN * 1.5 + LEFT * 1),
                          square_mobjects[9].animate.scale(1 / scale_factor),
                          square_mobjects[j + (j + 1)].animate.scale(1 / scale_factor), run_time=running_time(j))

                Result_two.to_corner(LEFT).shift(DOWN * 1)
                Results.add(Result)
                Results_two.add(Result_two)
            elif j < 4:
                self.play(Write(Calc), Write(Result), square_mobjects[9].animate.scale(scale_factor),
                          square_mobjects[j + (j + 1)].animate.scale(scale_factor), run_time=running_time(j))

                self.wait(running_time(j))

                self.play(Uncreate(Calc), Result.animate.next_to(Results[j - 1]),
                          square_mobjects[9].animate.scale(1 / scale_factor),
                          square_mobjects[j + (j + 1)].animate.scale(1 / scale_factor), run_time=running_time(j))

                Result_two.next_to(Results_two[j - 1])
                Results.add(Result)
                Results_two.add(Result_two)

            elif j >= 4 and j != 0:
                self.play(Write(Calc), Write(Result), square_mobjects[9].animate.scale(scale_factor),
                          square_mobjects[(j + 1) + (j + 2)].animate.scale(scale_factor), run_time=running_time(j))

                self.wait(running_time(j))

                self.play(Uncreate(Calc), Result.animate.next_to(Results[j - 1]),
                          square_mobjects[9].animate.scale(1 / scale_factor),
                          square_mobjects[(j + 1) + (j + 2)].animate.scale(1 / scale_factor), run_time=running_time(j))

                Result_two.next_to(Results_two[j - 1])
                Results.add(Result)
                Results_two.add(Result_two)

        return Results, Results_two

    def create_arrows_and_squares(self, square_mobject: Mobject, list_of_lists: np.ndarray):
        Square_Groups = VGroup()
        Arrow_Groups = VGroup()
        Brace_Groups = VGroup()
        Branch_one = self.moore_neighbours(0.7, list_of_lists, 1, to_branches=True).shift(UP * 2.5 + RIGHT * 1.5)
        Branch_two = self.moore_neighbours(0.7, list_of_lists, 2, to_branches=True).next_to(Branch_one, DOWN, buff=0.8)
        Branch_three = self.moore_neighbours(0.7, list_of_lists, 3, to_branches=True).next_to(Branch_two, DOWN,
                                                                                              buff=0.8)

        idx = 6
        Arrow_one = Arrow(start=square_mobject[idx * 3 - 2].get_center(), end=Branch_one[idx * 0].get_center(),
                          color=RED_E, buff=0.5, stroke_width=2)
        Arrow_two = Arrow(start=square_mobject[idx * 2 - 2].get_center(), end=Branch_two[idx * 0].get_center(),
                          color=RED_E, buff=0.5, stroke_width=2)
        Arrow_three = Arrow(start=square_mobject[idx * 1 - 2].get_center(), end=Branch_three[idx * 1].get_center(),
                            color=RED_E, buff=0.5, stroke_width=2)

        ## Labels
        label_one = MathTex(r"p_{j} = 63.3\%", font_size=30)
        label_one.move_to(Arrow_one.get_center())
        label_one.rotate(Arrow_one.get_angle())
        label_one.shift(UP * 0.2)

        label_two = MathTex(r"p_{j} = 8.56\%", font_size=30)
        label_two.move_to(Arrow_two.get_center())
        label_two.rotate(Arrow_two.get_angle())
        label_two.shift(DOWN * 0.2)

        label_three = MathTex(r"p_{j} = 0.16\%", font_size=30)
        label_three.move_to(Arrow_three.get_center())
        label_three.rotate(Arrow_three.get_angle())
        label_three.shift(UP * 0.2)

        Square_Groups.add(Branch_one, Branch_two, Branch_three)
        Arrow_Groups.add(Arrow_one, Arrow_two, Arrow_three)
        Brace_Groups.add(label_one, label_two, label_three)

        return Square_Groups, Arrow_Groups, Brace_Groups

    def create_large_grid(self, grid: np.ndarray, size: float):
        no_of_rows = grid.shape[0]
        no_of_columns = grid.shape[1]

        rect_group = VGroup()

        for row in range(no_of_rows):
            for column in range(no_of_columns):

                rect = Rectangle(height=size, width=size, stroke_width=0.1)

                # Position the rectangle based on its row and column
                rect.shift((column - no_of_columns // 2) * size * RIGHT)
                rect.shift((row - no_of_rows // 2) * size * UP)

                # Color the rectangle based on the value in the grid
                if grid[row, column] == 8:
                    cl = BLUE_C
                elif grid[row, column] == 7:
                    cl = TEAL_B
                elif grid[row, column] == 6:
                    cl = GREEN_A
                elif grid[row, column] == 5:
                    cl = YELLOW_A
                elif grid[row, column] == 4:
                    cl = GOLD_A
                elif grid[row, column] == 3:
                    cl = ORANGE
                elif grid[row, column] == 2:
                    cl = RED_A
                elif grid[row, column] == 1:
                    cl = RED_E
                else:
                    cl = MAROON_E

                # noinspection PyArgumentList
                rect.set_fill(color=cl, opacity=1.0)
                # Add the rectangle to the group
                # inspection PyArgumentList
                rect_group.add(rect)

        return rect_group

    def update_colors(self, rect_group, grid):
        no_of_rows = grid.shape[0]
        no_of_columns = grid.shape[1]

        # Iterate through each rectangle in the group and update its color
        for i, rect in enumerate(rect_group):
            # Calculate the row and column of this rectangle
            row = i // no_of_columns
            column = i % no_of_columns

            if grid[row, column] == 8:
                cl = BLUE_C
            elif grid[row, column] == 7:
                cl = TEAL_B
            elif grid[row, column] == 6:
                cl = GREEN_A
            elif grid[row, column] == 5:
                cl = YELLOW_A
            elif grid[row, column] == 4:
                cl = GOLD_A
            elif grid[row, column] == 3:
                cl = ORANGE
            elif grid[row, column] == 2:
                cl = RED_A
            elif grid[row, column] == 1:
                cl = RED_E
            else:
                cl = MAROON_E

            # Update the color of the rectangle
            rect.set_fill(color=cl, opacity=1)

        return rect_group

    def Automata_loop(self, length: int, choice: str, square_size: float, epochs: int):
        Grids = VGroup()
        length = length
        # def initialize_grid(self, lengths : int, choice : str, limit : int):
        # def apply_rules_2d(self, grid, heat_transfer_probability, temperature):
        Functions = Function()

        grid = Functions.initialize_grid(length, choice="circle", limit=8)
        initial_grid = np.copy(grid)
        grid_object = self.create_large_grid(grid[1:-1, 1:-1], size=square_size).to_corner(LEFT)

        for k in range(epochs):
            grid = Functions.apply_rules_2d(grid, heat_transfer_probability=1, temperature=1)
            grid_object = self.update_colors(grid_object, grid[1:-1, 1:-1]).to_corner(LEFT)
            if k % 2 == 0:
                Grids.add(grid_object.copy())

        ## Play loop
        for i in range(len(Grids)):
            loop = lambda i: 1.5 if i == 0 else 0.1
            if i == 0:
                self.play(FadeIn(Grids[0]), run_time=loop(i))
                self.wait()
            else:
                self.play(Transform(Grids[i - 1], Grids[i]), run_time=loop(i))

        self.wait(4)
        Black_rectangle = Rectangle(color=BLACK, height=15, width=20)
        self.play(FadeIn(Black_rectangle))

"""
Scene 5: Calculating entropy, ImageMobject Convolution, MovingCameraScene
To call this class call this in the command prompt: manim -p -qh Manimations.py EntropyConvolution
"""

class EntropyConvolution(MovingCameraScene):
    def construct(self):
        Title=Tex("The crux of the problem: Calculating entropy",font_size=40).to_corner(LEFT + UP)
        self.play(Write(Title))
        self.wait()

        strategy=self.create_strategy(Title, 1)
        self.play(FadeIn(strategy, shift=DOWN))
        self.wait(7)

        Title2=Tex("The process to do it").to_corner(LEFT + UP)
        self.play(Transform(Title, Title2), Uncreate(strategy))
        self.wait()
        Number_list=self.create_number_mobjects().to_corner(LEFT)
        self.play(Create(Number_list))
        self.play(Number_list.animate.shift(UP * 1))
        self.wait()

        Elements=self.create_add_mobjects()
        Elements.to_corner(LEFT).shift(DOWN * 1)
        self.play(Create(Elements))
        self.wait()
        

    def create_strategy(self, Title_Mobject,  square_size):
        Strats=VGroup()

        ## First thing to notice
        Strategy=Tex("Strategy", font_size=40).to_corner(UP+LEFT).next_to(Title_Mobject, DOWN * 2)
        Notice=Tex(r"A cell can have a maximum energy value $\Phi$ chosen from 0 to 255.", 
                  font_size=30).next_to(Strategy, DOWN * 0.4).shift(RIGHT * 0.2)

        Notice.next_to(Notice, DOWN * 1)
        Arrow_one=Tex(r"$\Rightarrow$").next_to(Notice, DOWN).rotate(-np.pi / 2)
        
        ## 2nd thing to notice  
        Notice_two=Tex("We can partision the grid into 2x2 matrices and find the entropy of each matrix.", font_size=30).next_to(Arrow_one,  DOWN *  1)
        Arrow_two=Tex(r"$\Rightarrow$").next_to(Notice_two, DOWN * 1).rotate(-np.pi / 2)

        ## 3rd thing to Notice
        Notice_three=Tex(r"The job is to find integer combinations such that $a+b+c+d = E \; \; \land \; \; 0\leq E \leq 4\Phi$",
                        font_size=30).next_to(Arrow_two, DOWN * 1)

        ## Make the Matrix 
        matrix=Matrix([["a", "b"], ["c", "d"]], v_buff=0.8, h_buff=0.9).next_to(Notice_three, DOWN * 0.8).scale(0.7)


        Strats.add(Strategy, Notice, Arrow_one, Notice_two, Arrow_two, Notice_three, matrix)
        

        return Strats

    def create_number_mobjects(self):
        number_lists = ["\\{", "0", "$,$", "1", "$,$", "2", "$,$", "3", "$,$",
                        "4", "$,$", "5", "$,$", "6", "$,$", "7", "$,$", "8", "\\}"]

        Number_Groups = VGroup()
        for x in range(len(number_lists)):
            Font_size = lambda x: 40 if x == 0 or x == (len(number_lists) - 1) else 35

            if x % 2 == 0 and (x == 0 or x != len(number_lists) - 1):
                elements = Tex(number_lists[x], font_size=Font_size(x))
                Number_Groups.add(elements)

            else:
                elements = Tex(number_lists[x], font_size=Font_size(x))
                Number_Groups.add(elements)

        for i in range(1, len(Number_Groups)):
            Number_Groups[i].next_to(Number_Groups[i-1], RIGHT * 0.65)

        ## Move the comments down
        for idx, mobject in enumerate(Number_Groups):
          
          if idx % 2 == 0 and idx != len(number_lists)-1 and idx != 0:
              mobject.shift(DOWN * 0.15)

        return Number_Groups

    def create_add_mobjects(self):
        Groups=VGroup()
        elements=["a", "+" ,"b", "+",  "c", "+", "d", "="]
        for i in range(len(elements)):

            if i==0:
                element=MathTex( elements[0] , font_size=40)
                Groups.add(element)
            elif i >= 1:
                element=MathTex( elements[i] ,font_size=40)
                element.next_to(Groups[i-1], RIGHT)
                Groups.add(element)

        return Groups


    
    




