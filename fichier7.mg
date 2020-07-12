spell toto(a, b)
    if(a == 0)
        counter b;
    end
    summon c = 0;
    c = toto(a-1, b-1);
    counter c;
    yell(666);
end

summon x = toto(3, 5);
yell(x);
