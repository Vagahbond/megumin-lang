
let fibonacci(n)

    if (n < 2)
        res =  n;
    else 
        res =  fibonacci(n - 1) + fibonacci(n - 2);
    end

    return res
end

out(fibonacci(20));
