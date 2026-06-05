from graph.workflow import graph

query = input("Enter research topic: ")

result = graph.invoke({
    "query": query
})

print("\n\nFINAL REPORT:\n")
print(result["final_report"])