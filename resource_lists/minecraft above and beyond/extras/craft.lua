while (true)
    do
    
    -- CLEAR SCREEN --
    term.setBackgroundColor(colors.black)
    term.clear()
    term.setCursorPos(1,1)
    
    -- MODE SELECT --
    print("What do you want to do?")
    print("[ Craft | Add | Exit ]")
    print()
    
    local input = read()
    print()
    
    if (string.lower(input) == "exit")
        then
        
        -- EXIT PROGRAM --
        print("Goodbye.")
        sleep(2)
        break
        
    elseif (string.lower(input) == "craft")
        then
        
        -- CALCULATE CRAFTS --
        print("Sorry, I haven't coded this part yet.")
        print("Maybe try coming back later?") -- !!! --
        
        sleep(2)
        
    elseif (string.lower(input) == "add")
        then
        
        -- INSERT MORE CRAFTS --
        
        print("What recipe do you want to teach me?")
        print()
        
        local folder = string.gsub(string.lower(read()), " ", "_")
        print()
        
        if (fs.exists("recipes/"..folder))
            then
            
            -- OVERWRITE FILE --
            print("It looks like I already know that one...")
            print("Would you like to overwrite it?")
            print("[ Y | N ]")
            print()
            
            input = read()
            print()
            
            if (not(string.lower(input) == "y"))
                then
                
                print("Alright.")
                sleep(1)
                print("Goodbye?")
                sleep(1)
                break
                
            else
                
                print("Alright then!")
                fs.delete("recipes/"..folder)
                print("recipes/"..folder.." has been deleted.")
                print()
                
            end
            
        end
        
        -- START WRITING TO FILE --
        fs.makeDir("recipes/"..folder)
        local file = fs.open("recipes/"..folder.."/items.txt", "w")
        local item = folder..": "
        
        print("How many items does this recipe create?")
        print()
        
        input = read()
        print()
        
        if (type(input) == "number")
            then
            
            print("That's not a number!")
            sleep(1)
            print("I'm leaving...")
            sleep(1)
            break
            
        end
        
        file.writeLine(item..input)
        
        while (true)
            do
            
            print("What items do you need for this recipe?")
            print("(You can also say 'exit' to finish)")
            print()
            
            item = string.gsub(string.lower(read()), " ", "_")
            print()
            
            if (item == "exit")
                then
            
                print("Thanks for teaching me :D")
                sleep(1)
                
                break
            
            end
            
            print("How many of them do you need?")
            print()
            
            input = read()
            print()
            
            if (type(input) == "number")
                then
                
                print("That's not a number!")
                sleep(1)
                print("I'm leaving...")
                sleep(1)
                break
                
            end
            
            input = input * -1
            file.writeLine(item..": "..input)
            
        end
        
        file.close()
        
        sleep(2)
                    
    else
        
        print("I don't know how to do that...")
        sleep(2)
        
    end
        
end

-- CLEAR SCREEN AGAIN --
term.clear()
term.setCursorPos(1,1)
