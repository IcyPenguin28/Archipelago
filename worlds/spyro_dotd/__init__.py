from .world import DotDWorld as DotDWorld

from multiprocessing import Process

from worlds.LauncherComponents import Component, components, icon_paths

def run_client():
    from .client import main
    Process(target=main,name="SpyroDotDClient").start()

icon_paths["spyro_dotd"] = f"ap:{__name__}/icon.png"
components.append(Component("Spyro DotD Client", func=run_client, icon="spyro_dotd"))