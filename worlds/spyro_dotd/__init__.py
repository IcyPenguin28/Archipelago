from .world import DotDWorld as DotDWorld

from multiprocessing import Process

from worlds.LauncherComponents import Component, components, icon_paths

def run_client():
    from .client import main
    Process(target=main,name="SpyroDotDClient").start()

icon_paths["spyro_dotd"] = f"ap:{__name__}/icon.png"
components.append(Component("Spyro DotD Client", func=run_client, icon="spyro_dotd"))

# Just wanna say, this was my first AP world,
# so if anything looks like it was copied directly from the comments of APQuest,
# that was just me taking notes basically.