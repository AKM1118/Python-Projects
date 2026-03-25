import turtle
drawer = turtle.Turtle()
drawer.right(120)
mode = {"tree" : 1, "triangle" : 2, "hexa cube":3, "triangle cube":4}
base_angle = drawer.heading()
drawer.speed(0)

def tree(length):
    if length < 10:                     # When length is less than 1, stop the recursion
        return
    else:
        drawer.forward(length)              # Draw the line
        drawer.left(30)                     # Rotate to the left
        tree(2*length/3)                    # Draw all the left branches
        drawer.right(60)                    # Rotate to the right
        tree(2*length/3)                    # Draw the right branch
        drawer.left(30)                     # Rotate the turtle to original rotation
        drawer.backward(length)             # Go back to local root

def triangle_cube(depth,size): # This function draws a triangle inside a cube inside a triangle, dunno how that happened but look cool
    if depth < 0:
        return

    px, py = drawer.xcor(), drawer.ycor()

    for i in range(3):
        drawer.forward(size / (2**depth))
        triangle_cube(depth-1,size)
        drawer.goto(px,py)
        drawer.right(120)


def hexa_cube(depth,size): # Draws a set of triangles that form a hexagon
    if depth < 0:
        return
    px, py = drawer.xcor(), drawer.ycor()
    for i in range(3):
        drawer.forward(size / (2**depth))
        drawer.right(120)
        hexa_cube(depth-1,size)
    drawer.teleport(px,py)

def triangle(depth ,points):

    drawer.penup()
    drawer.goto(points[0])
    drawer.pendown()
    drawer.goto(points[1])
    drawer.goto(points[2])
    drawer.goto(points[0])
    def midpoint(p1,p2):
        return (int((p1[0] + p2[0]) / 2),int((p1[1] + p2[1]) /2))

    if depth > 0:
        #drawer.penup()
        drawer.goto(points[0])
        triangle(depth-1, [points[0],midpoint(points[0],points[1]),midpoint(points[0],points[2])])
        triangle(depth-1, [midpoint(points[0],points[1]),points[1],midpoint(points[2],points[1])])
        triangle(depth-1, [midpoint(points[0],points[2]),midpoint(points[2],points[1]),points[2]])
def main():
    selector = mode.get("triangle")
    if selector == 0:
        tree(100)
    elif selector == 1:
        size = 300
        points = [(int(drawer.xcor()),int(drawer.ycor())), (int(size/2),int(size*(0.75**0.5))),(int(size),int(drawer.ycor()))]
        triangle(6,points)
    turtle.done()

main()