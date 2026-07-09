"""
Swarm Dynamics - Particle System with Springs and Global Forces
群體動力學：粒子 + 彈簧 + 旋轉/呼吸效果

    Args:
        N: Number of struts (default: 7)
        Prec: Coordinate precision (default: 3)
        Speed: Rotation speed (default: 0.6)
        Amp: Breathing amplitude (default: 0.0)
        Knn: K-nearest neighbors (default: 4)
        Radius: Connection radius (default: 0.0, unlimited)
        Stiff: Spring stiffness (default: 1.5)
        Damp: Damping coefficient (default: 0.12)
        Dt: Time step (default: 0.03)
        Act: Spring activation amplitude (default: 0.15)
        Seed: Random seed (default: 1)
        Box: Bounding box for generation
        Start: Start simulation
        Reset: Reset simulation

    Returns:
        L: Strut lines
        Links: Spring connection lines
        Nodes: Particle positions
        MidPts: Strut midpoints
        Labels: Strut length labels
        Lengths: Strut lengths
        t: Simulation time
        Frame: Frame count
        out: Debug messages
"""

from ghpythonlib.componentbase import executingcomponent as component
import Rhino.Geometry as rg
import random
import math


class SwarmDynamics(component):
    # Class variables to maintain state across calls
    _particles = None
    _springs = None
    _struts = None
    _base_lines = None
    _time_step = 0
    _frame = 0

    @staticmethod
    def set_seed(seed):
        """Set random seed"""
        if seed is not None:
            random.seed(int(seed))
        else:
            random.seed()

    @staticmethod
    def bbox_from_box(b):
        """Convert Box to BoundingBox"""
        if b is None:
            return rg.BoundingBox(rg.Point3d(-50, -50, 0), rg.Point3d(50, 50, 10))
        if isinstance(b, rg.Box):
            return b.BoundingBox
        if isinstance(b, rg.BoundingBox):
            return b
        return rg.BoundingBox(rg.Point3d(-50, -50, 0), rg.Point3d(50, 50, 10))

    @staticmethod
    def rand_coord(bb):
        """Generate random coordinate within bounding box"""
        return (
            random.uniform(bb.Min.X, bb.Max.X),
            random.uniform(bb.Min.Y, bb.Max.Y),
            random.uniform(bb.Min.Z, bb.Max.Z)
        )

    @staticmethod
    def rounded(c, nd=3):
        """Round coordinates"""
        return (round(c[0], nd), round(c[1], nd), round(c[2], nd))

    @staticmethod
    def vec_from_to(a, b):
        """Vector from point a to point b"""
        return rg.Vector3d(b.X - a.X, b.Y - a.Y, b.Z - a.Z)

    def initialize_system(self, N, Prec, Knn, Radius, Seed, Box):
        """Initialize the particle system"""
        msgs = []
        self.set_seed(Seed)
        msgs.append("系統初始化中...")

        bb = self.bbox_from_box(Box)

        # 1) Generate base struts
        uniq = set()
        base_lines = []
        tries = 0
        target = max(1, int(N))
        max_tries = max(200, target * 60)

        while len(base_lines) < target and tries < max_tries:
            tries += 1
            a = self.rounded(self.rand_coord(bb), Prec)
            b = self.rounded(self.rand_coord(bb), Prec)
            if a == b or a in uniq or b in uniq:
                continue
            uniq.add(a)
            uniq.add(b)
            base_lines.append(rg.Line(rg.Point3d(*a), rg.Point3d(*b)))

        msgs.append("生成了 {} 條桿件".format(len(base_lines)))

        # 2) Extract all nodes
        pts_set = set()
        for ln in base_lines:
            pts_set.add((ln.From.X, ln.From.Y, ln.From.Z))
            pts_set.add((ln.To.X, ln.To.Y, ln.To.Z))
        pts = [rg.Point3d(*p) for p in pts_set]

        msgs.append("總共 {} 個節點".format(len(pts)))

        # 3) Create particles with initial velocities
        particles = []
        for p in pts:
            vx = (random.random() - 0.5) * 0.1
            vy = (random.random() - 0.5) * 0.1
            vz = (random.random() - 0.5) * 0.05
            particles.append({
                "pos": rg.Point3d(p),
                "vel": rg.Vector3d(vx, vy, vz),
                "force": rg.Vector3d(0, 0, 0)
            })

        # 4) Build strut indices
        idx = {(p.X, p.Y, p.Z): i for i, p in enumerate(pts)}
        struts = []
        for ln in base_lines:
            i = idx.get((ln.From.X, ln.From.Y, ln.From.Z))
            j = idx.get((ln.To.X, ln.To.Y, ln.To.Z))
            if i is not None and j is not None and i != j:
                struts.append((i, j))

        # 5) Build nearest neighbor connections (springs)
        n = len(particles)
        edges = set()

        for i in range(n):
            pi = particles[i]["pos"]
            dists = []
            for j in range(n):
                if i == j:
                    continue
                pj = particles[j]["pos"]
                d = pi.DistanceTo(pj)
                if Radius <= 0.0 or d <= Radius:
                    dists.append((d, j))

            dists.sort(key=lambda x: x[0])
            for k in range(min(Knn, len(dists))):
                j = dists[k][1]
                a, b = (i, j) if i < j else (j, i)
                edges.add((a, b))

        # If no edges, use pure KNN
        if len(edges) == 0 and n > 1:
            msgs.append("使用純 KNN 連接")
            for i in range(n):
                pi = particles[i]["pos"]
                dists = [(pi.DistanceTo(particles[j]["pos"]), j)
                        for j in range(n) if i != j]
                dists.sort(key=lambda x: x[0])

                for k in range(min(Knn, len(dists))):
                    j = dists[k][1]
                    a, b = (i, j) if i < j else (j, i)
                    edges.add((a, b))

        # 6) Create springs
        springs = []
        for (a, b) in edges:
            L0 = particles[a]["pos"].DistanceTo(particles[b]["pos"])
            springs.append({
                "ij": (a, b),
                "L0": L0,
                "phi": random.uniform(0.0, 2.0 * math.pi)
            })

        msgs.append("彈簧數量: {}".format(len(springs)))

        # Store state
        SwarmDynamics._particles = particles
        SwarmDynamics._springs = springs
        SwarmDynamics._struts = struts
        SwarmDynamics._base_lines = base_lines
        SwarmDynamics._time_step = 0
        SwarmDynamics._frame = 0

        return msgs

    def simulate_step(self, Speed, Amp, Stiff, Damp, Dt, Act):
        """Run one simulation step"""
        if SwarmDynamics._particles is None or len(SwarmDynamics._particles) == 0:
            return

        particles = SwarmDynamics._particles
        springs = SwarmDynamics._springs

        # Update time
        SwarmDynamics._time_step += 1
        SwarmDynamics._frame += 1

        current_time = SwarmDynamics._time_step * Dt

        # Calculate center of mass
        cx = sum(p["pos"].X for p in particles) / len(particles)
        cy = sum(p["pos"].Y for p in particles) / len(particles)
        cz = sum(p["pos"].Z for p in particles) / len(particles)
        center = rg.Point3d(cx, cy, cz)

        # Global rotation
        if abs(Speed) > 0.001:
            rot_angle = Speed * current_time
            rot = rg.Transform.Rotation(rot_angle, rg.Vector3d(0, 0, 1), center)
        else:
            rot = rg.Transform.Identity

        # Calculate target positions (rotation + breathing)
        targets = []
        for p in particles:
            target = rg.Point3d(p["pos"])
            target.Transform(rot)
            if abs(Amp) > 0.001:
                breathing = Amp * math.sin(Speed * current_time)
                target.Z += breathing
            targets.append(target)

        # Reset forces
        forces = [rg.Vector3d(0, 0, 0) for _ in particles]

        # Calculate spring forces
        for spring in springs:
            i, j = spring["ij"]

            pi = particles[i]["pos"]
            pj = particles[j]["pos"]

            dir_ij = self.vec_from_to(pi, pj)
            dist = dir_ij.Length

            if dist < 1e-9:
                continue

            dir_ij.Unitize()

            # Dynamic natural length (active spring)
            L_dynamic = spring["L0"] * (1.0 + Act * math.sin(Speed * current_time + spring["phi"]))

            # Spring force F = k * (L - L0)
            force_mag = Stiff * (dist - L_dynamic)
            force_vec = dir_ij * force_mag

            forces[i] += force_vec
            forces[j] -= force_vec

        # Add attraction to targets
        attraction_strength = 0.1
        for i, p in enumerate(particles):
            to_target = self.vec_from_to(p["pos"], targets[i])
            forces[i] += to_target * attraction_strength

        # Update particles (Euler integration)
        damping = max(0.0, min(1.0, 1.0 - Damp))

        for i, p in enumerate(particles):
            p["vel"] *= damping
            acceleration = forces[i] * Dt
            p["vel"] += acceleration
            displacement = p["vel"] * Dt
            p["pos"] = p["pos"] + displacement

    def RunScript(self, N, Prec, Speed, Amp, Knn, Radius, Stiff, Damp, Dt, Act, Seed, Box, Start, Reset):
        ghenv.Component.Message = 'v{{version}}'

        # Default values
        N = N if N is not None else 7
        Prec = Prec if Prec is not None else 3
        Speed = Speed if Speed is not None else 0.6
        Amp = Amp if Amp is not None else 0.0
        Knn = Knn if Knn is not None else 4
        Radius = Radius if Radius is not None else 0.0
        Stiff = Stiff if Stiff is not None else 1.5
        Damp = Damp if Damp is not None else 0.12
        Dt = Dt if Dt is not None else 0.03
        Act = Act if Act is not None else 0.15
        Seed = Seed if Seed is not None else 1
        Start = Start if Start is not None else False
        Reset = Reset if Reset is not None else False

        msgs = []

        # Parameter validation
        if Act <= 0:
            Act = 0.12
            msgs.append("Act<=0，設為 0.12")
        if Dt <= 1e-6:
            Dt = 0.03
            msgs.append("Dt<=0，設為 0.03")
        if Damp >= 0.98:
            Damp = 0.12
            msgs.append("Damp>=0.98，設為 0.12")

        # Initialize or reset system
        need_rebuild = Reset or SwarmDynamics._particles is None

        if need_rebuild:
            init_msgs = self.initialize_system(N, Prec, Knn, Radius, Seed, Box)
            msgs.extend(init_msgs)

        # Run simulation
        if Start and SwarmDynamics._particles is not None:
            self.simulate_step(Speed, Amp, Stiff, Damp, Dt, Act)

        # Generate outputs
        L = []
        MidPts = []
        Labels = []
        Lengths = []

        if SwarmDynamics._particles and SwarmDynamics._struts:
            particles = SwarmDynamics._particles
            for (i, j) in SwarmDynamics._struts:
                if i < len(particles) and j < len(particles):
                    pi = particles[i]["pos"]
                    pj = particles[j]["pos"]
                    line = rg.Line(pi, pj)
                    L.append(line)
                    MidPts.append(line.PointAt(0.5))
                    length = line.Length
                    Lengths.append(length)
                    Labels.append("L={:.2f}".format(length))

        # Spring links
        Links = []
        if SwarmDynamics._springs and SwarmDynamics._particles:
            particles = SwarmDynamics._particles
            for spring in SwarmDynamics._springs:
                i, j = spring["ij"]
                if i < len(particles) and j < len(particles):
                    Links.append(rg.Line(particles[i]["pos"], particles[j]["pos"]))

        # Nodes
        Nodes = []
        if SwarmDynamics._particles:
            Nodes = [p["pos"] for p in SwarmDynamics._particles]

        # Time and frame
        t = SwarmDynamics._time_step * Dt if Dt > 0 else 0
        Frame = SwarmDynamics._frame

        # Debug messages
        msgs.extend([
            "狀態: {}".format("運行中" if Start else "暫停"),
            "節點: {}, 彈簧: {}, 桿件: {}".format(len(Nodes), len(Links), len(L)),
            "時間: {:.2f}s, 幀: {}".format(t, Frame),
            "參數: Act={:.3f}, Stiff={:.2f}, Damp={:.2f}".format(Act, Stiff, Damp)
        ])

        out = "\n".join(msgs)

        return (L, Links, Nodes, MidPts, Labels, Lengths, t, Frame, out)
