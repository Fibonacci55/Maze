# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from maze import Rectangular_Maze
from maze_gen_algorithms import Recursive_Backtracker
from maze_printer import Rectangular_Maze_Printer
import argparse
import networkx as nx



def get_edge_points (of_list):

    #of_list.sort()

    l_min = [of_list[0]]
    r_max = [of_list[0]]

    t_min = [of_list[0]]
    b_max = [of_list[0]]

    #print (len(of_list))
    for p in of_list:
        #print(p)
        if p[1] == l_min[0][1]:
            l_min.append(p)
        if p[1] < l_min[0][1]:
            l_min = [p]

        if p[1] == r_max[0][1]:
            r_max.append(p)
        if p[1] > r_max[0][1]:
            r_max = [p]

        if p[0] == t_min[0][0]:
            t_min.append(p)
        if p[0] < t_min[0][0]:
            t_min = [p]

        if p[0] > b_max[0][0]:
            b_max.append(p)
        if p[0] > b_max[0][0]:
            b_max = [p]
#
    return (l_min, t_min, r_max, b_max)

def make_a_path (point_list):
    pass


    l = args.path.split(" ")
    pl = []
    # print ("P", p)
    # print ("int(p[0].split(',')[0])", int(p[0].split(',')[0]))
    # print ("int(p[0].split(',')[1])", int(p[0].split(',')[1]))
    # print ("p[0].split(',')", p[0].split(','))
    # print ('int(p[0].split(',')[0])', int(p[0].split(',')[0]))
    p = l[0]
    print ('p', p)
    s = tuple((int(p.split(',')[0]), int(p.split(',')[1])))
    for p in l[1:]:
        e = tuple((int(p.split(',')[0]), int(p.split(',')[1])))
        print(s, e)
        pl += nx.dijkstra_path(m.grid_graph, s, e)
        s = e

    print(pl)
    p = Rectangular_Maze_Printer(cell_size=20, filename=args.svg_file)
    p.print(m)
    p.add_path(pl)
    p.save()


def create_arg_parser():
    parser = argparse.ArgumentParser(
                    prog = 'Maze',
                    description = 'Creates mazes',
                    epilog = ' ')

    parser.add_argument('-n', '--new', action="store_true", help='Create a new maze')
    parser.add_argument('-d', '--dimension', type=str,
                        dest="dimension", default='',
                        help='Dimension of the new mask' )

    parser.add_argument('-m', '--apply_mask', type=str,
                        dest="mask", default='',
                        help='Apply the mask on the maze' )
    parser.add_argument('-s', '--save_to', type=str,
                        dest="to_file", default='',
                        help='Save a newly created maze to file')
    parser.add_argument('-r', '--reload_from', type=str,
                        dest="from_file", default='',
                        help='Reload a created maze from file')
    parser.add_argument('-p', '--print_to', type=str,
                        dest="svg_file", default='',
                        help='Create a SVG file')

    parser.add_argument('-i', '--info', action="store_true", help='Info on a maze')

    parser.add_argument('-a', '--add', type=str,
                        dest="path", default='',
                        help='Add a path from two points to a maze. Given by "n,n n,n"')
    return parser

if __name__ == '__main__':

    #mask = "D:\\Projects\\Flavio\\fla_quadrat_low.png"
    #mask = "D:\\Projects\\Flavio\\fla_quadrat.png"
    #m = Rectangular_Maze(300,300)
    #m = Rectangular_Maze.masked(mask)
    #m = Rectangular_Maze(2,2)
    #a = Recursive_Backtracker()
    #a(m)
    #m.to_file('maze_1.txt')

    #m = Rectangular_Maze.from_file('saved_maze.txt')
    #p = Rectangular_Maze_Printer()
    #p.print(m, path_way=[(10, 12), (129, 100)])


    #import networkx as nx

    #print (r)

    #print (l)
    #p = nx.dijkstra_path(m.grid_graph, (10, 12), (129, 0))
    #print (p)

    #-m "D:\\Projects\\Flavio\\fla_quadrat.png" -p "maze.svg" -s "save_maze.txt"
    #-r "save_maze.txt"
    """-m
    "D:\Projects\Flavio\fla_quadrat_35.png" - s
    fla_quadrat_35.sav - p
    fla_quadrat_35.svg"""
    parser = create_arg_parser()
    args = parser.parse_args()

    if args.new:
        if args.dimension:
            w=int(args.dimension.split(',')[0])
            h=int(args.dimension.split(',')[1])
            m = Rectangular_Maze(w,h)
            a = Recursive_Backtracker()
            a(m)

    if args.mask:
        m = Rectangular_Maze.masked(args.mask)
        a = Recursive_Backtracker()
        a(m)

    if args.to_file:
       m.to_file(args.to_file)

    if args.from_file:
        m = Rectangular_Maze.from_file(args.from_file)
        m.make_graph()
        l = list(m.grid_graph.nodes)
        #print(l)
        if args.info:
            r = get_edge_points(l)
            print (r[0])
            print (r[1])
            print (r[2])
            print (r[3])
        if args.path:
            make_a_path(args.path)


    if args.svg_file and not args.path:
        p = Rectangular_Maze_Printer(filename=args.svg_file)
        p.print(m)
        p.save()

#-r "save_maze.txt" -a "32,12 130,99" -p "maze_1.svg"
#-n -d 10,10 -s square.sav -p square.svg
#-r square.sav -a "0,0 9,9" -p square_p.svg