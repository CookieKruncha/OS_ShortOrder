import subprocess
import json
import sys
import os
import glob
from concurrent.futures import ThreadPoolExecutor

def run_eval(scheduler, seeds, config):
    cmd = ["./start.sh", "evaluate", scheduler, "--seeds", seeds, "--config", config, "--json"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return config, json.loads(res.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error on {config}: {e.stderr}", file=sys.stderr)
        return config, None

def main():
    scheduler = sys.argv[1] if len(sys.argv) > 1 else "my-scheduler"
    configs = sorted([os.path.basename(c) for c in glob.glob("configs/*.toml")])
    
    dev_seeds = "1000..1039"
    holdout_seeds = "2000..2039"
    
    print(f"Benchmarking {scheduler} on DEV ({dev_seeds}) and HOLDOUT ({holdout_seeds})")
    print(f"{'Profile':<20} | {'Dev Score':<15} | {'Dev CI':<10} | {'Holdout Score':<15} | {'Holdout CI':<10} | {'Rejects (D/H)':<15}")
    print("-" * 100)
    
    total_dev = 0
    total_holdout = 0
    
    with ThreadPoolExecutor(max_workers=4) as ex:
        dev_f = {config: ex.submit(run_eval, scheduler, dev_seeds, config) for config in configs}
        hol_f = {config: ex.submit(run_eval, scheduler, holdout_seeds, config) for config in configs}
        
        for config in configs:
            _, dev_res = dev_f[config].result()
            _, hol_res = hol_f[config].result()
            
            dev_score = dev_res["summary"]["mean_score"] if dev_res else 0
            dev_ci = dev_res["summary"]["score_ci95"] if dev_res else 0
            dev_rej = dev_res["summary"]["invalid_assignments"] if dev_res else 0
            
            hol_score = hol_res["summary"]["mean_score"] if hol_res else 0
            hol_ci = hol_res["summary"]["score_ci95"] if hol_res else 0
            hol_rej = hol_res["summary"]["invalid_assignments"] if hol_res else 0
            
            total_dev += dev_score
            total_holdout += hol_score
            
            print(f"{config:<20} | {dev_score:<15.2f} | ±{dev_ci:<9.2f} | {hol_score:<15.2f} | ±{hol_ci:<9.2f} | {dev_rej}/{hol_rej:<13}")
            
    mean_dev = total_dev / len(configs)
    mean_holdout = total_holdout / len(configs)
    print("-" * 100)
    print(f"{'MEAN':<20} | {mean_dev:<15.2f} | {'':<10} | {mean_holdout:<15.2f} | {'':<10} |")

if __name__ == '__main__':
    main()
