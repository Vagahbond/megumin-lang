let toto(a, b)
    if(a == 0)
        return b;
    end
    var c = 0;
    c = toto(a-1, b-1);
    return c;
    out(666);
end

var x = toto(3, 5);
out(x);
