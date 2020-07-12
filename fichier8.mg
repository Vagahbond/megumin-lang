summon a = 2;

yell(a);

summon b = <~a;

yell(b);

b = 5;

yell(b);

yell(a);


spell toto(a, b)
    yell(a + b);
end

toto(a, b);

summon toto_2 = <~toto;

toto_2(a, b);

toto = 70;

yell(toto);