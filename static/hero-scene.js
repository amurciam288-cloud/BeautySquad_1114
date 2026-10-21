// Decorative-only Three.js scene. The page remains complete if this module or WebGL fails.
const canvas = document.querySelector("[data-three-scene]");

if (canvas && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  import("https://cdn.jsdelivr.net/npm/three@0.171.0/build/three.module.js")
    .then(({
      AmbientLight,
      Color,
      DirectionalLight,
      Group,
       CatmullRomCurve3,
       Mesh,
       MeshPhysicalMaterial,
       PerspectiveCamera,
      Points,
      PointsMaterial,
      BufferGeometry,
      Float32BufferAttribute,
       Scene,
       SphereGeometry,
       TubeGeometry,
       Vector3,
       WebGLRenderer,
    }) => {
      const container = canvas.parentElement;
      const compact = window.matchMedia("(max-width: 760px)").matches;
      const scene = new Scene();
      scene.background = new Color(0x9f3f6d);
      const camera = new PerspectiveCamera(32, 1, 0.1, 100);
      camera.position.set(0, 0, 6.8);

      let renderer;
      try {
        renderer = new WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: "low-power" });
      } catch {
        return;
      }
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, compact ? 1.2 : 1.5));

      scene.add(new AmbientLight(0xffddea, 1.8));
      const keyLight = new DirectionalLight(0xfff5e8, 4.2);
      keyLight.position.set(-3, 4, 5);
      scene.add(keyLight);
      const blushLight = new DirectionalLight(0xf08ab5, 2.8);
      blushLight.position.set(4, -2, 3);
      scene.add(blushLight);

       const sculpture = new Group();
       const pearl = new Mesh(
         new SphereGeometry(compact ? 1.24 : 1.38, compact ? 32 : 48, compact ? 24 : 36),
         new MeshPhysicalMaterial({
          color: 0xf7b9d0,
          metalness: 0.12,
          roughness: 0.18,
          clearcoat: 1,
          clearcoatRoughness: 0.1,
          iridescence: 0.8,
          iridescenceIOR: 1.45,
          iridescenceThicknessRange: [160, 520],
        })
      );
      pearl.scale.set(0.82, 1.25, 0.82);
      pearl.rotation.set(0.12, -0.28, -0.08);
       sculpture.add(pearl);

      const haloMaterial = new MeshPhysicalMaterial({
        color: 0xffdbe8,
        metalness: 0.72,
        roughness: 0.2,
        clearcoat: 1,
        clearcoatRoughness: 0.14,
        emissive: 0x6d173f,
        emissiveIntensity: 0.12,
      });
       function createOrganicRing(radius, height, depth, tubeRadius, segments) {
         const points = [];
         for (let index = 0; index < 16; index += 1) {
           const angle = (index / 16) * Math.PI * 2;
           const variation = 1 + Math.sin(angle * 3 + radius) * 0.018;
           points.push(new Vector3(
             Math.cos(angle) * radius * variation,
             Math.sin(angle) * height * variation,
             Math.sin(angle * 2 + radius) * depth
           ));
         }
         const curve = new CatmullRomCurve3(points, true, "centripetal");
         return new Mesh(new TubeGeometry(curve, segments, tubeRadius, compact ? 5 : 7, true), haloMaterial);
       }

       const halo = createOrganicRing(1.72, 1.02, 0.08, 0.027, compact ? 64 : 96);
       halo.rotation.set(1.16, 0.18, -0.25);
       sculpture.add(halo);
       const haloSecond = createOrganicRing(1.48, 0.82, 0.06, 0.019, compact ? 56 : 84);
       haloSecond.rotation.set(0.28, -0.82, 0.52);
       haloSecond.scale.set(1.16, 0.78, 1);
       sculpture.add(haloSecond);
      sculpture.position.set(0.18, 0.02, 0);
      scene.add(sculpture);

      const particleCount = compact ? 22 : 42;
      const particlePositions = [];
      for (let index = 0; index < particleCount; index += 1) {
        const angle = (index / particleCount) * Math.PI * 2;
        const radius = 1.9 + (index % 5) * 0.16;
        particlePositions.push(
          Math.cos(angle) * radius,
          Math.sin(angle * 1.7) * 1.65,
          Math.sin(angle) * 0.6 - 0.2
        );
      }
      const particleGeometry = new BufferGeometry();
      particleGeometry.setAttribute("position", new Float32BufferAttribute(particlePositions, 3));
      scene.add(new Points(
        particleGeometry,
        new PointsMaterial({ color: 0xffe9b8, size: compact ? 0.045 : 0.055, transparent: true, opacity: 0.72, sizeAttenuation: true })
      ));

      function resize() {
        const { width, height } = container.getBoundingClientRect();
        if (!width || !height) return;
        renderer.setSize(width, height, false);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
      }

      const resizeObserver = new ResizeObserver(resize);
      resizeObserver.observe(container);
       resize();
       renderer.setAnimationLoop((time) => {
         const seconds = time * 0.001;
         sculpture.position.x = 0.18 + Math.sin(seconds * 0.21) * 0.025;
         sculpture.position.y = 0.02 + Math.sin(seconds * 0.31) * 0.055;
         sculpture.rotation.y = Math.sin(seconds * 0.18) * 0.08;
         sculpture.rotation.x = Math.sin(seconds * 0.24 + 0.6) * 0.035;
         sculpture.rotation.z = Math.sin(seconds * 0.16) * 0.018;
         sculpture.scale.setScalar(1 + Math.sin(seconds * 0.27 + 0.8) * 0.008);
         pearl.rotation.z = Math.sin(seconds * 0.34) * 0.035 - 0.08;
         pearl.rotation.y = Math.sin(seconds * 0.22 + 1.2) * 0.025 - 0.28;
         halo.rotation.z = -0.25 + Math.sin(seconds * 0.2) * 0.035;
         haloSecond.rotation.z = 0.52 + Math.sin(seconds * 0.17 + 1) * 0.045;
         renderer.render(scene, camera);
       });
    })
    .catch(() => {
      // CSS shapes remain visible when the CDN or WebGL is unavailable.
      canvas.hidden = true;
    });
}
