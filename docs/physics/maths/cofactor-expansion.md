# The Cofactor Expansion
You'll often need to find the determinant of a matrix. For a 2 by 2 matrix, you can use this formula, but for bigger matrices, this will not work.

The cofactor expansion works for *any* square matrix, which are the only ones that *have* determinants. Let's see how it works.

## The Checkerboard

![Cofactor Grid](/img/manim/cofactor-grid.png)

If you remember only just this checkboard, you can still have a good idea of how to do the cofactor expansion.

## The Technique

You can expand the section below to see a textual description of how to do the cofactor expansion; however, I believe you'll find it more intuitive to just watch the animation instead.

<details>
    <summary>The details...</summary>

    Start off by choosing any column or row to expand along. Zeroes are very simple to expand; if you find them, expand along them.

    For *each* element along the row or column, ignore all elements that share a vertical or horizontal line with it. We only care about the element we're expanding, the off-axis elements, and remember that *checkerboard*? We'll also want the sign that corresponds to our element we're expanding.

    You should now have a sub-matrix, one isolated element, and the corresponding sign from the checkerboard. **Multiply these all together**.

    When you add up all the expansions along *one* row or column, the result is the determinant.

    Confused? Have a look at the animation below.

</details>

