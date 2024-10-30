function Spline2

  pkg load symbolic
  close all; clc;
  n = input('Введіть кількість інтервалів (n): ');
  a = input('Введіть початок інтервалу (a): ');
  b = input('Введіть кінець інтервалу (b): ');

  func = input('Введіть функцію для інтерполяції (наприклад, @(x) exp(x)): ');

  figure;
  cubic_B_spline_interpolation(func, a, b, n);

end

function cubic_B_spline_interpolation(f, a, b, n)


    x_nodes = linspace(a, b, n+1);
    h = (b - a) / n;


    syms x;
    f_sym = f(x);
    f_prime = diff(f_sym, x);


    a_sym = vpa(a);
    b_sym = vpa(b);

    a1 = double(subs(f_prime, x, a_sym));
    b1 = double(subs(f_prime, x, b_sym));


    y_nodes = arrayfun(f, x_nodes);


    A = zeros(n+1, n+1);
    b_vec = zeros(n+1, 1);


    for i = 2:n
        A(i, i-1:i+1) = [1/6, 2/3, 1/6];
        b_vec(i) = y_nodes(i);
    end


    A(1, 1) = -1/2;
    A(1, 3) = 1/2;
    A(n+1, n-1) = -1/2;
    A(n+1, n+1) = 1/2;
    b_vec(1) = a1 * h;
    b_vec(end) = b1 * h;


    alpha = A \ b_vec;


    function val = spline_func(xi)
        val = 0;
        for i = 1:n+1
            val = val + alpha(i) * B_basis(xi, x_nodes, i, h);
        end
    end


    function B = B_basis(x, x_nodes, i, h)
        xi = (x - x_nodes(i)) / h;
        if abs(xi) <= 1
            B = (1/6)*((2 - abs(xi))^3 - 4*((1 - abs(xi))^3));
        elseif abs(xi) <= 2
            B = (1/6) * (2 - abs(xi))^3;
        else
            B = 0;
        end
    end

    m = n+30;

    x_extra = linspace(a, b, m);
    S = zeros(size(x_extra));

    for j = 1:length(x_extra)
        S(j) = spline_func(x_extra(j));
    end

    y_exp = zeros(size(x_extra));
    for j = 1:length(x_extra)
        y_exp(j) = f(x_extra(j));
    end

    %y_exp = arrayfun(f, x_extra); %Можна так

    plot(x_extra, S, 'r-', 'LineWidth', 2);
    hold on;
    plot(x_extra, y_exp, 'b--', 'LineWidth', 2);
    plot(x_nodes, y_nodes, 'bo', 'MarkerSize', 6, 'MarkerFaceColor', 'b');
    title('B-сплайн інтерполяція та оригінальна функція');
    xlabel('x');
    ylabel('S(x) та f(x)');
    legend('B-сплайн', 'Оригінальна функція', 'Вузли');
    grid on;
    hold off;
end


