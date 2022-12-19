import turtle
hr = turtle.Turtle()
hr.left(90)
hr.speed(0)

def tree(length):
    if length < 10:                     # When length is less than 1, stop the recursion
        return
    else:
        hr.forward(length)              # Draw the line
        hr.left(30)                     # Rotate to the left
        tree(2*length/3)                # Draw all the left branches
        hr.right(60)                    # Rotate to the right
        tree(2*length/3)                # Draw the right branch
        hr.left(30)                     # Rotate the turtle to original rotation
        hr.backward(length)             # Go back to local root

tree(100)

turtle.done()