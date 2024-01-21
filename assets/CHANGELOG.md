- port to py3
- added new guid for typehints (extrusion and pointcloud) and modified the old ones for str, float, ghdoc, and none.

- [?] propose type-hint for component hints instead of the metadata (?)
- [?] propose to have the "out" parameter as out and set to false by default in the metadata.json (guid out param: 3ede854e-c753-40eb-84cb-b48008f14fd4)


doubts:
- I have doubts about the  utility of setting the "SourceCount" in the metadata.json. I think it is not necessary, since the number of inputs is already defined by the number of parameters in the function. I think it is to leave it by deafult to 0.
