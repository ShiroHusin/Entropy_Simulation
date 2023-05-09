import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.cm
from manim import *
from scipy.special import comb
from scipy import signal
import random

Grid_data = np.load(r'C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\grids.npy')
Prime_data = np.load(r'C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\prime_grids.npy')
loaded_entropies = np.load(r'C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\entropies.npy')

microstate_data=pd.read_csv(r"C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\Microstate_dataframe.csv")

class check_grid:
    def __init__(self, yes=False):
        self.animation=yes

    def Animation(self):
        if self.animation==True:

            plt.style.use("dark_background")
            fig, (ax, ax2)=plt.subplots(1,2, figsize=(10,5), width_ratios=[1.2, 0.98])

            im=ax.imshow(Grid_data[0, :, :], cmap="plasma", vmin=np.min(Grid_data[0, :, :]), vmax=np.max(Grid_data[0, :, :]))
            im2=ax2.imshow(Prime_data[0, :, :], cmap="binary", vmin=0, vmax=1)
            fig.colorbar(im, ax=ax, label="Intensity", shrink=0.56)

            ax.axis("off")
            ax2.axis("off")

            def animate(frame):
                im.set_data(Grid_data[frame, :, :])
                im2.set_data(Prime_data[frame, :, :])

                ax.set_title(f"Temp: {1.0}", loc="left")
                ax.set_title(f"Epoch: {frame}", loc="right")
                ax2.set_title("Non-Prime locations")

            ani=FuncAnimation(fig,animate, frames=Grid_data.shape[0], repeat=False, interval=80)
            plt.show()

        else:
            pass

bug_checking=check_grid(yes="no")
bug_checking.Animation()

# Function to convert grid data to RGB image using colormap
def convert_to_rgb_image(grid_data, cmap="plasma", vmin=0, vmax=16):
    cmap = matplotlib.colormaps.get_cmap(cmap)
    norm = plt.Normalize(vmin, vmax)
    grid_data_rgb = cmap(norm(grid_data))
    return (grid_data_rgb[:, :, :3] * 255).astype(np.uint8)

# Convert Grid_data to RGB image using colormap
Grid_copies=Grid_data.shape[0]
Grid_data_rgb = np.array([convert_to_rgb_image(Grid_data[i, :, :], cmap=plt.get_cmap("plasma")) for i in range(Grid_copies)])

Gird=Grid_data_rgb[0, :, :, 0]/255

def setup(Grid_data, entropy_array):
    start=0
    stop=(Grid_data.shape[0]-1) * 4
    step=4
    entropy=np.array(entropy_array)
    x_index = np.arange(start, stop + step, step)

    return start, stop, x_index, entropy

start, end, x_index, entropy= setup(Grid_data, loaded_entropies)
"""
Scene 1: Grid simulation
Manim Section
Manim command for low quality: manim -p -ql Image.py ImageFromArray 
Manim command for medium quality: manim -p -qm Image.py ImageFromArray
Manim command for high quality: manim -p -qh Image.py ImageFromArray
Note: your_class is changed to what class object you want to render
"""
class ImageFromArray(Scene):
    def construct(self):
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

                title = Tex(r"This is a Cellular Automata (CA) grid")
                title.to_corner(UP + LEFT)

                self.play(Write(title), Write(image_label))

                self.wait()
                transform_title = Tex(r"That is using CA to show increasing entropy")
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

class GameRules(Scene):
    def construct(self):
        # Set the number of rows and columns for the grid
        rows = 5
        columns = 5

        # Set the size of each square
        square_size = 0.5

        # Create a Group to store the squares and numbers
        grid_group = VGroup()

        # Create a NumPy array with the numbers you want to display
        numbers_array = np.random.randint(0, 10, size=(rows, columns))

        # Iterate through each row and column to create the grid
        for row in range(rows):
            for column in range(columns):
                # Create a square
                square = Square(side_length=square_size)

                # Position the square based on its row and column
                square.shift((column - columns // 2) * square_size * RIGHT)
                square.shift((row - rows // 2) * square_size * UP)

                # Get the number from the NumPy array
                number = numbers_array[row, column]

                # Create a Tex object for the number
                number_tex = Tex(str(number))

                # Position the number at the center of the square
                number_tex.next_to(square, direction=ORIGIN, buff=0)

                # Add the square and number to the grid_group
                grid_group.add(square)
                grid_group.add(number_tex)

        # Add the grid_group to the scene
        self.play(FadeIn(grid_group))
        self.wait()

