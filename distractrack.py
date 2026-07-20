import json, random

def run(seed=29):
    rng=random.Random(seed); naive_last=8.; aware_last=8.; velocity=1.; naive=aware=0; frames=[]
    for t in range(42):
        target=8+t if t<22 else 10+t
        distractor=50-t if t<22 else 8+t
        candidates=[(distractor+rng.uniform(-.25,.25),0),(target+rng.uniform(-.25,.25),1)]
        n=min(candidates,key=lambda item:abs(item[0]-naive_last))[0]
        predicted=aware_last+velocity
        a=min(candidates,key=lambda item:abs(item[0]-predicted)+3*(1-item[1]))[0]
        naive+=abs(n-target)<2; aware+=abs(a-target)<2
        velocity=.75*velocity+.25*(a-aware_last); naive_last=n; aware_last=a
        frames.append({"frame":t,"target":round(target,1),"distractor":round(distractor,1),
                       "aware":round(a,1)})
    return {"recency_accuracy":round(naive/42,3),"distractor_aware_accuracy":round(aware/42,3),
            "tracking_gain_pct":round(100*(aware-naive)/42,1),"timeline":frames[::6]}

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
