# buildout.extendssubs
A buildout extension that enables substitution of assignments for extends option.

Normally buildout doesn't seem to take command-line assignment options into account when working with the ``buildout:extends`` option. ``buildout.extendssubs`` provides an option ``extends-subs`` that works exactly the same as ``extends`` option and also can substitue assignment variables. ``extends-subs`` can work together with ``extends`` option, in this case config files in ``extends`` option will be loaded first.

Installation and Usage
======================

Check out source code from github.

    $ git clone https://github.com/vietdt/buildout.extendssubs.git
    $ cd buildout.extendssubs/
    
Update buildout.cfg to list the package directory as a develop egg to be built.

    [buildout]
    develop = .
    parts =
    
It's a bit tricky and run the buildout once with the develop egg defined but without the extension option. This is because extensions are loaded before the buildout creates develop eggs. We needed to use a separate buildout run to create the develop egg.

    $ ./bin/buildout -v
    
Now we can add the ``extensions`` and ``extends-subs`` options. Normally, when eggs are loaded from the network (TODO), we wouldn’t need to do the previous step.

    [buildout]
    develop = .
    extensions = buildout.extendssubs
    extends-subs = ${:LEVEL}.cfg

Then run the buildout again with assignment option set from command-line.

    $ ./bin/buildout -v buildout:LEVEL=staging
    
