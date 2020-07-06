var a = 1;



a = 2;



let fibonacci(n)

    if (n < 2)
        return n;
    else 
        return  fibonacci(n - 1) + fibonacci(n - 2);
    end

end

let outstuff()
    out(5);
end

out(fibonacci(20));
outstuff();

