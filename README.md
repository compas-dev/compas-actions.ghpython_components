# GHPython Componentizer

> A github action to make Grasshopper development 165% <sup><small>[1]</small></sup> version-control friendlier and 83% more pleasant.

Imagine if you could write your grasshopper components in Python code (both IronPython for RhinoV7 and less, or CPython for RhinoV8) in an actual text file with a powerful editor?
Git wouldn't hate you and life would be so much beautiful. 🐵

Well, here's an action for you then! 🦸‍♀️

---

## Usage

### Usage from Github Actions

The recommended way to use this tool is as a Github Action.
It needs to be run on a windows runner and IronPython/NuGet or Python3/pythonnet/Nuget depending of which component you want to build, needs to be pre-installed.

Copy the following workflow code into a `.github/workflows/main.yml` file in your repository.
Make sure you have the components definition (see below for details) stored in a source folder.
Replace the `source` and `target` to match your folder structure.
To specify the interpreter to use, you can define the action parameter `interpreter` to either `ironpython` or `python3` (by default it is `ironpython`).

For IronPython (RhinoV7 and less):

```yaml
on: [push]

jobs:
  build_ipy_ghuser_components:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: NuGet/setup-nuget@v1.0.5

      - name: Install IronPython
        run: |
          choco install ironpython --version=2.7.8.1

      - uses: compas-dev/compas-actions.ghpython_components@v5
        with:
          source: components
          target: build

      # The components have been built at this step.
      # Now you can choose what to do with them, e.g.:
      # upload them as artifacts:
      - uses: actions/upload-artifact@v2
        with:
          name: ipy_ghuser-components
          path: build
```

For Python3 (RhinoV8):

```yaml
on: [push]

jobs:
  build_cpy_ghuser_components:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: NuGet/setup-nuget@v1.0.5

      - name: Install CPython and pythonnet package
        run: |
          choco install python --version=3.9.10
          python -m pip install pythonnet==3.0.3

      - uses: compas-dev/compas-actions.ghpython_components@v5
        with:
          source: components
          target: build
          interpreter: cpython  # optional, defaults to ironpython

      - uses: actions/upload-artifact@v2
        with:
          name: cpy_ghuser-components
          path: build
```

For IronPython2 (RhinoV8):

```yaml
on: [push]

jobs:
  build_ipy_ghuser_components:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: NuGet/setup-nuget@v1.0.5

      - name: Install IronPython
        run: |
          choco install ironpython --version=2.7.8.1

      - uses: compas-dev/compas-actions.ghpython_components@v5
        with:
          source: components
          target: build
          interpreter: ipy_v2

      # The components have been built at this step.
      # Now you can choose what to do with them, e.g.:
      # upload them as artifacts:
      - uses: actions/upload-artifact@v2
        with:
          name: ipy_ghuser-components
          path: build
```


Commit, push and enjoy! 🍿

### Usage on the command line

Alternatively, you can also use this tool directly from the command line.
Make sure to have IronPython or Python3/pythonnet installed and the `GH_IO.dll` assembly available.
Then start the script pointing it to a source and target folder, e.g.:

    ipy componentize_ipy.py examples/ipy build
    ipy componentize_ipy_v2.py examples/ipy_v2 build
    python componentize_cpy.py examples/cpy build

Optionally, tag it with a version:

    ipy componentize_ipy.py examples/ipy build --version 0.1.2
    ipy componentize_ipy_v2.py examples/ipy_v2 build --version 0.1.2
    python componentize_cpy.py examples/cpy build --version 0.1.2

An optional name prefix can help tell components apart from other similarly named ones:

    ipy componentize_ipy.py examples/ipy build --prefix "(PACKAGE-NAME)"
    ipy componentize_ipy.py examples/ipy_v2 build --prefix "(PACKAGE-NAME)"
    python componentize_cpy.py examples/cpy build --prefix "(PACKAGE-NAME)"

## How to create components

1. Create a folder to contain your components
1. Each component goes into its own folder
1. The name of the folder determines the name of the `.ghuser` file created
1. Inside the component folder:
   1. Create a `metadata.json` file containing all required details of the component
   1. Add a lovely icon named `icon.png` (24x24)
   1. Add a `code.py` file with the Python script of the component
1. Use this action setting `source` and `target` folder inputs
1. Be happy 🎈

## Where are the generated components?

This action stores the generated components under the `target` folder, but these files only exist for the duration of the build.
After that -if no further steps are taken- they will be automatically deleted.

The simplest option to keep the generated files is to use the `actions/upload-artifact@v2` action and upload them as artifacts. Check [this for more details](https://github.com/actions/upload-artifact) and in particular, [the details about where to find the uploaded artifacts](https://github.com/actions/upload-artifact#where-does-the-upload-go).

An alternative is to include them in your packaging steps, e.g. calling `python setup.py clean --all sdist bdist_wheel` right after having generated the components (and assuming your setup is configured accordingly, will pick up the components and add them to the pip package. This is a very convenient way that ensures the components are always released from a clean state. An example of this is available on the [release workflow of COMPAS](https://github.com/compas-dev/compas/blob/main/.github/workflows/release.yml).

## Specification

### Icon

* Icon name should be `icon.png`
* Icon dimensions should be `24x24`

## Python code

Supports a small set of templated variables that can be used in code:
  * `{{version}}`: Gets replaced with the version, if specified in the command-line.
  * `{{name}}`: Gets replaced with the name of the component as defined in the metadata file.
  * `{{ghuser_name}}`: Gets replaced with the name of the `.ghuser` file being generated.

## Metadata

* `name`: Name of the component. Keep it short, single words are best.
* `nickname`: Abbreviation of the component. Keep it short, 1~5 character words are best.
* `category`: Category of the component. The category controls in which tab the component will end up.
* `subcategory`: Subcategory for this component. The subcategory controls in which panel the component will end up.
* `description`: **(optional)** Description of the component. Be succinct but clear.
* `exposure`: **(optional)** Controls where the component will be exposed. Defaults to `2` (primary). Accepts one of the following integer values:
  * `-1`:  Hidden. Do not expose the object anywhere.
  * `2`: Primary. Expose the object in the first section on the toolbar.
  * `4`: Secondary. Expose the object in the second section on the toolbar.
  * `8`: Expose the object in the third section on the toolbar.
  * `16`: Expose the object in the fourth section on the toolbar.
  * `32`: Expose the object in the fifth section on the toolbar.
  * `64`: Expose the object in the sixth section on the toolbar.
  * `128`: Expose the object in the seventh section on the toolbar.
* `instanceGuid`: **(optional)** Statically define a GUID for this instance. Defaults to a new Guid.
* `ghpython`
  * `hideOutput`: **(optional ⚠️ only IronPython)** Defines whether to hide or not `out` output parameter. Defaults to `True`.
  * `hideInput`: **(optional ⚠️ only IronPython)** Defines whether to hide or not the `code` input parameter. Defaults to `True`.
  * `isAdvancedMode`: **(optional ⚠️ only IronPython)** Defines whether the script is in advanced mode (aka GH_Component SDK mode) or procedural mode. Defaults to `False`.
  * `marshalOutGuids`: **(optional ⚠️ only IronPython)** Defines whether output Guids will be looked up or not. Defaults to `True`. Change to `False` to preserve output Guids.
  * `marshalGuids`: **(optional ⚠️ only CPython)** Defines whether input Guids will be looked up or not. Defaults to `True`. Change to `False` to preserve input Guids.
  * `iconDisplay`: **(optional)** Defines whether to display the icon or not. Defaults to `0`.
    * `0` : Application setting
    * `1` : Text display
    * `2` : Icon display
  * `inputParameters`: List of input parameters.
    * `name`: Name of the input parameter.
    * `nickname`: **(optional)** Abbreviation of the input parameter. Defaults to the same as `name`.
    * `description`: **(optional)** Description of the input parameter.
    * `optional`: **(optional)** Defines whether the input parameter is optional or not. Defaults to `True`.
    * `allowTreeAccess`: **(optional)** Defines whether to allow tree access for this input parameter. Defaults to `True`.
    * `showTypeHints`: **(optional)** Defines whether to show type hints for this input parameter. Defaults to `True`.
    * `scriptParamAccess`: **(optional)** Defines access type of the parameter. Defaults to `item`. Accepts either integer value or string value.
      * `0` / `item`: item access
      * `1` / `list`: list access
      * `2` / `tree`: tree access
    * `wireDisplay`: **(optional)** Defines wire display type. Accepts either integer value or string value.
      * `0` / `default`: Wire display is controlled by the application settings.
      * `1` / `faint`: Wires are displayed faintly (thin and transparent) while the parameter is not selected.
      * `2` / `hidden`: Wires are not displayed at all while the parameter is not selected.
    * `typeHintID`: **(optional)** Defines the type hint of the input parameter. Defaults to `ghdoc`.
      Accepts either a Guid value or a string value. The following are the valid
      string values (their respective Guids are not listed here for readability):
      `none`, `ghdoc`, `float`, `bool`, `int`, `complex`, `str`, `datetime`, `guid`,
      `color`, `point`, `vector`, `plane`, `interval`, `uvinterval`, `box`, `transform`,
      `line`, `circle`, `arc`, `polyline`, `rectangle`, `curve`, `mesh`, `surface`, `subd`, `brep`, `pointcloud`, `geometrybase`.
    * `reverse`: **(optional)** Defines whether data inside the parameter is reversed. Defaults to `False`.
    * `simplify`: **(optional)** Defines whether data inside the parameter is simplified. Defaults to `False`.
    * `flatten`: **(optional)** Defines whether data inside the parameter is flattened. Mutually exclusive with `graft`. Defaults to `False`.
    * `graft`: **(optional)** Defines whether data inside the parameter is grafted. Mutually exclusive with `flatten`. Defaults to `False`.
  * `outputParameters`: List of output parameters.
    * `name`: Name of the output parameter.
    * `nickname`: **(optional)** Abbreviation of the output parameter. Defaults to the same as `name`.
    * `description`: **(optional)** Description of the output parameter.
    * `optional`: **(optional)** Defines whether the output parameter is optional or not. Defaults to `False`.
    * `reverse`: **(optional)** Defines whether data inside the parameter is reversed. Defaults to `False`.
    * `simplify`: **(optional)** Defines whether data inside the parameter is simplified. Defaults to `False`.
    * `flatten`: **(optional)** Defines whether data inside the parameter is flattened. Mutually exclusive with `graft`. Defaults to `False`.
    * `graft`: **(optional)** Defines whether data inside the parameter is grafted. Mutually exclusive with `flatten`. Defaults to `False`.

## Caveats

GHUser components have one important limitation: once used in a document, they forget who they are.
The don't know they were created out of a `ghuser` component, they will be simple GHPython components.
This has an important consequence: **if you update the `ghuser` components,
those already in use will NOT be automatically updated**.

## License

This package is maintained by Gramazio Kohler Research [@gramaziokohler](https://github.com/gramaziokohler)
and it is published under an [MIT License](LICENSE).

---
> <sup>[1] Like, totally scientifically proven. word.</sup>
