domain mixing {
    symbols {
        predicates:
            flour/1,
            sugar/1,
            batter/1,
            whisk/1,
            sponge/1,
            mixer/1,
            container/1,
            in/2,
            on/2,
            inHand/2,
            handEmpty/1,
            robotAt/1,
            clean/1,
            graspable/1,
            ingredient/1,
            hand/1,
            location/1,
            wipePred/3;

        constants:
	    glass1, glass2,
	    knife1, knife2,
	    fork1, fork2,
	    spoon1, spoon2,
	    plate1, plate2, 
            cup1, cup2,
	    saucer1, saucer2,
	    napkin1, napkin2,
            
	    bowl1, bowl2,
            i1, i2, i3,
            m1,
            w1,
            s1,
            left, right,
            table1, cupboard1, shelf1;
    }

    action wipe(?x, ?y, ?z) {
        preconds:
            !K(clean(?y)) &
            K(sponge(?z)) &
            K(inHand(?z, ?x)) &
            K(robotAt(?y)) & 
            K(hand(?x)) &
            K(location(?y)) &
            K(graspable(?z))

        effects:
            add(Kf, clean(?y)),
            add(Kf, wipePred(?x,?y,?z))
    }

    problem wiping-problem {
        initdb {
            Kf:
                !K(clean(table1)) &
                K(sponge(s1)) &
                K(inHand(s1, left)) &
                K(robotAt(table1)) & 
                K(hand(left)) &
                K(location(table1)) &
                K(graspable(s1))
        }

        goal:
	        K(wipePred(?x, table1, ?z))
    }
}

