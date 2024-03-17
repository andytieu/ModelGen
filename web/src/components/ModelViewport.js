import {Canvas, useFrame, useLoader } from '@react-three/fiber';
import {MarchingCubes, MarnchigCube, Environment, Bounds, CameraControls, Sphere, useGLTF, TransformControls} from '@react-three/drei';
import { CreatureBody } from './creature-body/CreatureBody';

export const ModelViewport = () => {
    const {nodes, materials} = useGLTF("/assets/modelgenhead.glb");

    return (
        <Canvas dpr={[1, 1.5]} camera={{position: [0, 0, -8], fov: 30}}>
            <CameraControls />
            <TransformControls />

            <ambientLight intensity={1} />
            <pointLight position={[1, 1, -1]} intensity={2} />
            <pointLight position={[-2, 2, 1]} intensity={1} />
            <color attach="background" args={["#f0f0f0"]} />

            {/* <MarchingCubes resolution={80} maxPolyCount={100_000} enableColors>
                <meshStandardMaterial vertexColors thickness={0.15} roughness={0} />
                <CreatureBody params={[1, 1.5, [1, 1, 1]]} />
                {/* <MarchingCube strength={0.25} subtract={2} color={"#00f"} position={[0.2, 0.2, 0.2]} /> *}
            </MarchingCubes> */}

            {/* <Sphere args={[0.5]}>
                <meshPhongMaterial
                    color="#f00"
                />
            </Sphere> */}
            <mesh
                castShadow
                receiveShadow
                geometry={nodes.Plane.geometry}
                scale={[0.125, 0.125, 0.125]}
            >
                <meshPhongMaterial
                    color="#f3f3f3"
                />
            </mesh>
        </Canvas>
    )
};