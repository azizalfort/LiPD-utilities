function [newName] = makeUniqueStrings(name, protected)



if verLessThan('matlab','R2014a')
    if nargin<2
        newName = genvarname(name);
    else
        newName = genvarname(name,protected);
    end
else
    if nargin<2
        newName = matlab.lang.makeUniqueStrings(name);
    else
        newName = matlab.lang.makeUniqueStrings(name,protected);
        
    end
    
end