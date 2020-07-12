var a = 2;

out(a);

var b = <~a;

out(b);

b = 5;

out(b);

out(a);


let toto(a, b)
    out(a + b);
end

toto(a, b);

var toto_2 = <~toto;

toto_2(a, b);

toto = 666;

out(toto);