def compareMenteeWithMentor(menteeCSV, mentorsCSV):
    comparisons = []
    
    for _, mentor in mentorsCSV.iterrows():
        comparison = {
            "mentee_name": menteeCSV["name"],
            "mentor_name": mentor["name"],
            "domain_match": menteeCSV["research_domain"].lower() == mentor["research_domain"].lower(),
            "mentee_subdomain": menteeCSV["subdomain"],
            "mentor_subdomain": mentor["subdomain"]
        }
        
        comparisons.append(comparison)
        
    return comparisons
