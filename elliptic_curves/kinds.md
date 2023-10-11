# Weierstrass

$y^2 = x^3 + a * x + b$
$4 * a^3 + 27 * b^2 \ne 0$

$l = \frac{y_p - y_q}{x_p - x_q}$
$l = \frac{3*x_p^2 + a}{2*y_p}$

$x_r = l^2 - x_p - x_q$
$y_r = -y_p + l *(x_p - x_r)$


# Montgomery

$b* y^2 = x^3 + a * x^2 + x$

$l = \frac{y_p - y_q}{x_p - x_q}$
$l = \frac{3 * x_p^2 + 2 * a * x_p + 1}{2 * b * y_p}$

$x_r = b * l^2 - a - x_p - x_q$
$y_r = l * (2 * x_p + x_q + a) - b * l^3 - y_p$

# Edwards

$a * x^2 + y&2 = c^2 * (1 + d * x^2 * y^2)$ if char is not 2
$c * d * (1 - c^4 * d) \ne 0$

$x_r = \frac{x_p * y_q + x_q * y_p}{1 + d * x_p * x_q * y_p * y_q}$
$y_r = \frac{y_p * y_q - x_q * x_p}{1 - d * x_p * x_q * y_p * y_q}$


# Edwards -> Montgomery
if $a = 1, c^2 = 1$:

$e = 1 - d$
$u = \frac{1 + y}{1 - y}$
$v = \frac{2 * (1 + y)}{x * (1 - y)}$

Montgomery: $e^{-1}* v^2 = u^3 + (4 * e^{-1} - 2) * u^2  + u$

# Montgomery -> Edwards 

$a = \frac{A + 2}{B}$
$d = \frac{A - 2}{B}$

$u = \frac{x}{y}$
$v = \frac{x - 1}{x + 1}$

# Montgomery -> Weierstrass

$divide\ every\ coeff\ by\ B^3$

$u = \frac{x}{B}$
$v = \frac{y}{B}$

$v^2 = u^3 + \frac{A}{B}* u^2 + B^{-2}*u$

$u -> t - \frac{A}{3B}$

$v^2 = t^3 + \frac{3 - A^2}{3B^2} * t + \frac{2*A^3 - 9 * A}{27*B^3}$


$t = \frac{x}{B} + \frac{A}{3B}$
$v = \frac{y}{B}$
$a = \frac{3 - A^2}{3B^2} $
$b = \frac{2*A^3 - 9 * A}{27*B^3}$


# Weierstrass -> Montgomery

$v^2 = t^3 + a * t + b$

$\alpha ^ 3 + a * \alpha + b = 0$
$3 * \alpha^2 + a$ - qresidue
$s = \sqrt{3 * \alpha^2 + a)}^{-1}$

$x = s * (t - \alpha)$
$y = s * v$
$A = 3 * \alpha * s$
$B = s$
