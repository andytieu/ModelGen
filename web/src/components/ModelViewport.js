import {Canvas, useFrame} from '@react-three/fiber';
import {MarchingCubes, MarchingCube, Environment, Bounds, CameraControls, Sphere} from '@react-three/drei';
import { CreatureBody } from './creature-body/CreatureBody';

export const ModelViewport = () => {
    return (
        <Canvas dpr={[1, 1.5]} camera={{position: [0, 0, 2], fov: 30}}>
            <CameraControls />

            <ambientLight intensity={1} />
            <pointLight position={[0.5, 0.5, 0.5]} intensity={2} />
            <pointLight position={[-1, 1, 0.5]} intensity={1} />
            <color attach="background" args={["#f0f0f0"]} />

            {/* <MarchingCubes resolution={80} maxPolyCount={100_000} enableColors>
                <meshStandardMaterial vertexColors thickness={0.15} roughness={0} />
                <CreatureBody params={[1, 1.5, [1, 1, 1]]} />
                {/* <MarchingCube strength={0.25} subtract={2} color={"#00f"} position={[0.2, 0.2, 0.2]} /> *}
            </MarchingCubes> */}

            <group>
                <meshStandardMaterial vertexColors thickness={0.15} roughness={0} />

                <Sphere args={[1]} />
            </group>
        </Canvas>
    )
};