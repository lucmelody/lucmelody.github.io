template<class T> struct UnrealArray
{
    T* Data;
    unsigned long Length;
    unsigned long Max;
};
 
struct UnrealObject
{
    unsigned char Unknown [0x2C];
    unsigned long NameIndex;
};
 
struct UnrealName
{
    unsigned char Unknown [0x10];
    char Name [1];
};
void Dump ( void )
{  
    FILE * pFile;
    pFile = fopen ("log.txt","w");
    DoRtlAdjustPrivilege();
    EnumProcessAddresses(GetCurrentProcess(), ScanAddressRange);
    UnrealArray<UnrealObject*>* GlobalObjects;
    UnrealArray<UnrealName*>* GlobalNames;
    GlobalObjects = (UnrealArray<UnrealObject*>*) offsetGobj;
    GlobalNames = (UnrealArray<UnrealName*>*) offsetNameList;
    printf("Count=0x%x\n", GlobalObjects->Length);
    for ( unsigned long i = 0; i < GlobalObjects->Length; i++ )
    {
        if ( !GlobalObjects->Data [i] )
        continue;
        unsigned long NameIndex = GlobalObjects->Data [i]->NameIndex;
        if ( NameIndex < 0 || NameIndex > GlobalNames->Length )
        continue;
        if ( !GlobalNames->Data [NameIndex] )
        continue;
        fprintf ( pFile, "Object[%06i] %s\n", i, GlobalNames->Data [NameIndex]->Name );
    }
    printf("Count=0x%x\n", GlobalNames->Length);
    for ( unsigned long i = 0; i < GlobalNames->Length; i++ )
    {
        if ( !GlobalNames->Data [i] )
            continue;
        fprintf ( pFile, "Name[%06i] %s\n", i, GlobalNames->Data [i]->Name );
    }
    fclose(pFile);
    printf("Dump Complete\n", GlobalNames->Length);
}
 
CHAR* Object_Name = "Name";
CHAR* Object_Outer = "Outer";
CHAR* Object_Class = "Class";
CHAR* Object_Object = "Object";
void Dump2()
{
    printf("Start Dump2...\n");
    FILE * Log;
    Log = fopen ("log.txt","a");
    UnrealArray<UnrealObject*>* ObjectManager;
    UnrealArray<UnrealName*>* NameManager;
    ObjectManager = (UnrealArray<UnrealObject*>*) offsetGobj;
    NameManager = (UnrealArray<UnrealName*>*) offsetNameList;
    // Static character arrays for the string compares
    // Some storage pointers for saved values
    int Object_Start = 0;
    DWORD Object_ClassPtr = 0x0;
    DWORD Offset_Max = 0x150;
    DWORD Offset_MaxObjects = 0x4;
    DWORD Offset_Name = 0x2C;
    DWORD Offset_Outer = 0x0;
    DWORD Offset_Class = 0x0;
    DWORD Offset_PropertyOffset = 0x0;
    DWORD Offset_PropertySize = 0x0;
    printf("First Search...\n");
    // Loop the object table
    for ( unsigned long i = 0; i < ObjectManager->Length; i++ )
    {
        DWORD Object = (DWORD) ObjectManager->Data[i];
        // Check if the object is valid
        if ( !Object )
            continue;
        // Get the name index
        DWORD Name = *(PDWORD) ( (DWORD) Object + (DWORD) Offset_Name );
        // Find the Name UProperty
        if ( strcmp ( NameManager->Data[Name]->Name, Object_Name ) == 0 )
        {
            printf("found NAME...\n");
        // Scan the range of bytes to the size of Offset_Max
            for ( DWORD j = Offset_Name - 0x2C; j < Offset_Max; j++ )
            {
                DWORD Offset = *(PDWORD) ( (DWORD) Object + (DWORD) j );
                // Check if the offset matches the UObject->Name offset
                if ( Offset == Offset_Name )
                {
                    // Store the PropertyOffset offset
                    Offset_PropertyOffset = j;
                    // Take the current object index and move it back a few entries
                    // Outer starts before Name so we have to do this for the next loop
                    Object_Start = i - (Offset_Max / 4);
                    goto JmpOne;
                }
             }
        }
    }
    // Check if we found a PropertyOffset offset
    JmpOne:
    if ( !Offset_PropertyOffset )
    {
        printf("Not found!\n");
        return;
    }
    printf("Second Search...\n");
    // Loop the object table
    for ( unsigned long i = Object_Start; i < ObjectManager->Length; i++ )
    {
        DWORD Object = (DWORD) ObjectManager->Data[i];
        // Check if the object is valid
        if ( !Object )
            continue;
        // Get the name index
        DWORD Name = *(PDWORD) ( (DWORD) Object + (DWORD) Offset_Name );
        if ( !Offset_Outer )
        {
            // Check if the object name matches Object_Outer
            if ( strcmp ( NameManager->Data[Name]->Name, Object_Outer ) == 0 )
            // Get the relative offset for the property
            Offset_Outer = *(PDWORD) ((DWORD) Object + (DWORD) Offset_PropertyOffset);
        }
        if ( !Offset_Class )
        {
            // Check if the object name matches Object_Class
            if ( strcmp ( NameManager->Data[Name]->Name, Object_Class ) == 0 )
            // Get the relative offset for the property
            Offset_Class = *(PDWORD) ((DWORD) Object + (DWORD) Offset_PropertyOffset);
        }
    }
    // Check if we found both the outer and class offsets
    if ( !Offset_Outer || !Offset_Class )
    {
        printf("Not found!\n");
        return;
    }
    printf("Third Search...\n");
    // Loop the object table
    for ( unsigned long i = 0; i < ObjectManager->Length; i++ )
    {
        DWORD Object = (DWORD) ObjectManager->Data[i];
        // Check if the object is valid
        if ( !Object )
        continue;
        DWORD ObjectName = *(PDWORD) ( (DWORD) Object + (DWORD) Offset_Name );
        DWORD Class = *(PDWORD) ( (DWORD) Object + (DWORD) Offset_Class );
        DWORD ClassName = *(PDWORD) ( (DWORD) Class + (DWORD) Offset_Name );
 
        // Compare if the class and object name match that of the UObject UClass
        if ( ( strcmp ( NameManager->Data[ClassName]->Name, Object_Class ) == 0 ) && ( strcmp ( NameManager->Data[ObjectName]->Name, Object_Object ) == 0 ) )
        {
            // Found the UClass instance for UObject
            Object_ClassPtr = Object;
            goto JmpTwo;
        }
    }
    // Check if we got a valid UClass instance
    JmpTwo:
    if ( !Object_ClassPtr )
    {
        printf("Not found!\n");
        return;
    }
    printf("Fourth Search...\n");
    // Loop for the size of MaxObjects
    for ( unsigned long i = 0; i < Offset_MaxObjects; i++ )
    {
        // Create the predicted class size variable
        DWORD Temp = ( Offset_Class + 0x4 + ( i * 0x4 ) );
        // Scan the range of bytes to the size of Offset_Max
        for ( unsigned long j = Offset_Class; j < Offset_Max; j++ )
        {
            DWORD Offset = *(PDWORD) ( (DWORD) Object_ClassPtr + (DWORD) j );
            // Compare the value to the predicted class size
            if ( Offset == Temp )
            {
                // Found possible PropertySize offset
                Offset_PropertySize = j;
                goto JmpThree;
            }
        }
    }
    // Check if we found a PropertySize offset
    JmpThree:
    if ( !Offset_PropertySize )
    {
        printf("Not found!\n");
        return;
    }
    // Log the resulting values
    fprintf ( Log, "\nUObject:\n" );
    fprintf ( Log, "\t- Outer\t\t\t0x%X\n", Offset_Outer );
    fprintf ( Log, "\t- Name\t\t\t0x%X\n", Offset_Name );
    fprintf ( Log, "\t- Class\t\t\t0x%X\n", Offset_Class );
    fprintf ( Log, "\nUProperty:\n" );
    fprintf ( Log, "\t- PropertyOffset\t0x%X\n", Offset_PropertyOffset );
    fprintf ( Log, "\nUStruct:\n" );
    fprintf ( Log, "\t- PropertySize\t\t0x%X\n", Offset_PropertySize );
    fclose(Log);
    printf("Dump2 Done.\n");
}

