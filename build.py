# import argparse
import os
from typing import Dict, Tuple, List

from pylib.calculator_producer import calculator_producers
from pylib.editor_producer import editor_producers
from pylib.gz_compressor_producer import gz_compressor_producers
from pylib.imagepack import item_image_producers
from pylib.landing_page_producer import landing_page_producers
from pylib.producer import Producer, Scheduler, SingleFile, GenericProducer, producer_copyfile
from pylib.producer_plugins import plugins_producers
from pylib.typescript_producer import typescript_producer
from pylib.uglifyjs import uglify_js_producer
from pylib.yaml_linter_producer import resource_list_parser_producers


# CLI Argument Flags
# FLAG_skip_js_lint = False
# FLAG_skip_index = False
# FLAG_skip_gz_compression = False
# FLAG_skip_image_compress = False
# FLAG_force_image = False
# FLAG_skip_plugins = False


################################################################################
# core_resource_producers
#
# Create the producers definitions for all of the core resources found in the
# `./core` folder. These are essentially static files that might go through
# a small amount of processing, such as minification or compilation, but are
# not dynamic as most of the other files are.
################################################################################
def core_resource_producers() -> List[GenericProducer]:
    # Files that should be copied out of the "core" folder.
    copyfiles = [
        "core/calculator.css",
        "core/logo.png",
        "core/.htaccess",
        "core/add_game.png",
        "core/ads.txt",
        "core/favicon.ico",
    ]

    # Typescript Projects that should be compiled into javascript.
    ts_project_configs = [
        "core/src/tsconfig.json"
    ]

    # Javascript files that should be minified for production.
    uglify_js_files = [
        "cache/calculator.js",
        "core/yaml_export.js",
    ]

    core_producers: List[GenericProducer] = []

    # Add a producer for each file that will be copied over to output/.
    for copyfile in copyfiles:
        core_producers.append(
            Producer(
                input_path_patterns={
                    "file": "^{}$".format(copyfile),
                },
                paths=core_resource_paths,
                function=producer_copyfile,
                categories=["core"]
            )
        )

    # Add a producer for each of the typescript project files.
    for ts_project_config in ts_project_configs:
        core_producers.append(typescript_producer(ts_project_config, ["core"]))

    # Add a producer for each javascript file to minify.
    for uglify_js_file in uglify_js_files:
        core_producers.append(
            uglify_js_producer(
                input_file=uglify_js_file,
                output_file=os.path.join("output", os.path.basename(uglify_js_file)),
                categories=["core"]
            )
        )

    return core_producers


################################################################################
# core_resource_paths
#
# The paths generator for all of the core resources that get copied over from
# the core/ folder to the output/ folder directly.
################################################################################
def core_resource_paths(input_files: SingleFile, groups: Dict[str, str]) -> Tuple[SingleFile, SingleFile]:
    return (
        input_files,
        {
            "file": os.path.join("output", os.path.basename(input_files["file"]))
        }
    )


################################################################################
# main
#
# The main process for the build.py script. Handles argument parsing and
# starting up the generator process.
################################################################################
def main() -> None:
    # parser = argparse.ArgumentParser(
    #     description='Compile resourcecalculator.com html pages.'
    # )

    # parser.add_argument('limit_files', nargs='*', help="Speed up dev-builds by only building a specific set of one or more calculators")

    # parser.add_argument('--watch', action='store_true', help="Watch source files and automatically rebuild when they change")
    # parser.add_argument('--draft', action='store_true', help="Enable all speed up flags for dev builds")

    # # parser.add_argument('--no-jslint', action='store_true', help="Speed up dev-builds by skipping linting javascript files")
    # parser.add_argument('--no-uglify-js', action='store_true', help="Speed up dev-builds by skipping javascript compression")
    # parser.add_argument('--no-gz', action='store_true', help="Speed up dev-builds by skipping gz text compression")
    # parser.add_argument('--no-index', action='store_true', help="Speed up dev-builds by skipping building the index page")
    # parser.add_argument('--no-image-compress', action='store_true', help="Speed up dev-builds by skipping the image compresson")
    # parser.add_argument('--no-plugins', action='store_true', help="Skip plugin publication to get only the plain calculators")

    # parser.add_argument('--force-html', action='store_true', help="Force the html pages to be rebuilt even if they are newer then their source files")
    # parser.add_argument('--force-image', action='store_true', help="Force images to be rebuilt even if they are newer then their source files")

    # global FLAG_skip_index
    # # global FLAG_skip_js_lint
    # global FLAG_skip_gz_compression
    # global FLAG_skip_image_compress
    # global FLAG_force_image
    # global FLAG_skip_plugins

    # args = parser.parse_args()
    # if (args.watch):
    #     pass

    # # if args.no_jslint or args.draft:
    #     # FLAG_skip_js_lint = True

    # # if args.no_uglify_js or args.draft:
    # #     set_skip_uglify_flag()

    # if args.no_gz or args.draft:
    #     FLAG_skip_gz_compression = True

    # if args.no_image_compress or args.draft:
    #     FLAG_skip_image_compress = True

    # if args.no_index or args.draft:
    #     FLAG_skip_index = True

    # if args.force_image:
    #     FLAG_force_image = True

    # if args.no_plugins or args.draft:
    #     FLAG_skip_plugins = True

    # calculator_page_sublist = []
    # if len(args.limit_files) >= 1:
    #     FLAG_skip_index = True
    #     calculator_page_sublist = args.limit_files
    #     print("Only building", ", ".join(calculator_page_sublist))

    producers: List[GenericProducer] = []

    producers += resource_list_parser_producers()
    producers += item_image_producers()
    producers += calculator_producers()
    producers += editor_producers()
    producers += core_resource_producers()
    producers += landing_page_producers()
    producers += plugins_producers()
    producers += gz_compressor_producers()

    studio = Scheduler(
        producer_list=producers,
        initial_filepaths=Scheduler.all_paths_in_dir(
            base_dir=".",
            ignore_paths=["venv_docker", "venv", ".git", "node_modules", "output_master"]
        )
    )


    # build_producer_calls(producers, ["venv_docker", "venv", ".git", "node_modules"])

    # if args.watch:
    #     # If the watch argument is given then poll for changes of the files
    #     # polling is used instead of something like inotify because change
    #     # events are not propagated for volumes being run on docker for
    #     # windows. If ever a nicer solution for handling this appears this
    #     # code can be changed to support it.
    #     #
    #     # NOTE: With this polling method there is a race condition that is
    #     # possible to hit rather if saving frequently. If a file is
    #     # updated during its generation, after it has been read but before
    #     # the first file is written then it will not be detected in the
    #     # next pass-through.
    #     time.sleep(.5)
    #     continue
    # else:
    #     break


PROFILE = False
if __name__ == "__main__":

    if PROFILE:
        import cProfile
        import pstats

        with cProfile.Profile() as pr:
            main()

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.dump_stats(filename="profiledata.prof")
        # Useful to use snakeviz to display profile data `snakeviz profiledata.prof`
    else:
        main()
