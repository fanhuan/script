class kover_model(object)
    """A learnt model by kover. It have the following properties:
    Attributes:
        order: An integer representing the order of the rule in the model
        AorP: A string for absence or presence
        importance: An float for the importance of the rule
        kmer: A string for the kmer used to represent the rule
    """
    def __init__(self,order,AorP,importance,kmer):
        """Return a kover_model object whose id is *id*, AorP is *AorP*, importance
        is *importance* and kmer is *kmer*"""

        self.id = order
        self.AorP= AorP
        self.importance = importance
        self.kmer = kmer
