t="""| Dead Tube Coral Block        |    49 |       2 |         0 |
| Yellow Glazed Terracotta     |    39 |      37 |        18 |
| Purple Glazed Terracotta     |    26 |       8 |         0 |
| Magenta Glazed Terracotta    |    25 |      12 |         0 |
| Purple Wool                  |    25 |       2 |         1 |
| Sponge                       |    23 |      23 |         0 |
| Light Grey Glazed Terracotta |    22 |      22 |         0 |
| Block of Copper              |    13 |      13 |         5 |
| Red Glazed Terracotta        |     9 |       9 |         2 |
| Honeycomb Block              |     8 |       8 |         0 |
| Exposed Copper               |     6 |       6 |         0 |
| Blue Glazed Terracotta       |     4 |       4 |         0 |
| Crimson Planks               |     4 |       4 |         0 |
| Dead Bubble Coral Block      |     4 |       4 |         0 |
| Mangrove Planks              |     4 |       4 |         0 |
| Pink Terracotta              |     4 |       4 |         0 |
| Yellow Terracotta            |     4 |       4 |         0 |
| Birch Planks                 |     3 |       3 |         0 |
| Cherry Planks                |     3 |       3 |         0 |
| Chiselled Sandstone          |     3 |       3 |         0 |
| Diorite                      |     3 |       3 |         0 |
| Bedrock                      |     2 |       2 |         0 |
| Blue Ice                     |     2 |       2 |         0 |
| Blue Wool                    |     2 |       2 |         0 |
| Brown Wool                   |     2 |       2 |         0 |
| Exposed Cut Copper           |     2 |       2 |         0 |
| Light Grey Terracotta        |     2 |       2 |         0 |
| Nether Bricks                |     2 |       2 |         0 |
| Packed Ice                   |     2 |       2 |         0 |
| Polished Andesite            |     2 |       2 |         0 |
| Weathered Copper             |     2 |       2 |         0 |
| White Concrete               |     2 |       2 |         0 |
| White Terracotta             |     2 |       2 |         0 |
| Chiselled Red Sandstone      |     1 |       1 |         0 |
| Coarse Dirt                  |     1 |       1 |         0 |
| Dripstone Block              |     1 |       1 |         0 |
| End Stone Bricks             |     1 |       1 |         0 |
| Glowstone                    |     1 |       1 |         0 |
| Light Blue Concrete          |     1 |       1 |         0 |
| Light Blue Glazed Terracotta |     1 |       1 |         0 |
| Mud                          |     1 |       1 |         0 |
| Oak Planks                   |     1 |       1 |         0 |
| Red Sandstone                |     1 |       1 |         0 |
| Soul Soil                    |     1 |       1 |         0 |""".split('\n')

tmp=[i.split('|') for i in t]
tmp2=[]
for u in tmp:
    tmp2.append([u[1],u[3]])

o=[]
for i in tmp2:
    o.append("|".join(i).strip())
print("\n".join(o))