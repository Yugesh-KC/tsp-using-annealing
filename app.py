import pygame
import sys
import tsplib95
import time
from anneal import find_best_path

def save_tsp_file(nodes, filename="output.tsp"):
    with open(filename, "w") as f:
        f.write("COMMENT : User-drawn TSP problem\n")
        f.write("TYPE : TSP\n")
        f.write(f"DIMENSION : {len(nodes)}\n")
        f.write("EDGE_WEIGHT_TYPE : EUC_2D\n")
        f.write("NODE_COORD_SECTION\n")
        
        for i, (x, y) in enumerate(nodes, start=1):
            f.write(f"{i} {x} {y}\n")
        
        f.write("EOF\n")

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("TSP Node Drawer")
    clock = pygame.time.Clock()
    
    nodes = []
    best_route = []
    running = True
    
    while running:
        screen.fill((255, 255, 255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                nodes.append((x, y))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(nodes) > 1:  # Only compute if we have at least 2 nodes
                    save_tsp_file(nodes)
                    print("TSP file saved as output.tsp")
                    best_route, best_route_distance, convergence_time = find_best_path("output.tsp")
                    
                    if isinstance(best_route[0], list):  # Flatten if nested
                        best_route = best_route[0]

                    print("Best Route:", best_route)
                    print("Best Route Distance:", best_route_distance)
                    print("Convergence Time:", convergence_time)
        
        # Draw nodes and labels
        for i, (x, y) in enumerate(nodes, start=1):
            pygame.draw.circle(screen, (0, 0, 255), (x, y), 5)
            font = pygame.font.Font(None, 24)
            text = font.render(str(i), True, (0, 0, 0))
            screen.blit(text, (x + 5, y - 5))
        
        # Draw best route lines
        if best_route and len(best_route) > 1:
            for i in range(len(best_route) - 1):
                start_node = nodes[best_route[i] - 1]
                end_node = nodes[best_route[i + 1] - 1]
                pygame.draw.line(screen, (255, 0, 0), start_node, end_node, 2)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
