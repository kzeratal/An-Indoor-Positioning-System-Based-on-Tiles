import tileLoc
import database

if __name__ == "__main__":
    #database.create_database("original", 1000)
    #tileLoc.match_database_itself()
    tileLoc.match_local("A45", "A45")
'''
    database.create_crop_database("smooth9", 150)
    tileLoc.exp01c("smooth9", 2.25, 150, "A150C")
    database.create_crop_database("smooth9", 125)
    tileLoc.exp01c("smooth9", 1.875, 125, "A125C")
'''