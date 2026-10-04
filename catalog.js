window.PHAT_SKILLS = [
  {
    "name": "ask-workflow",
    "category": "Core workflow",
    "title": "Find your next step",
    "description": "ให้ agent อ่านสถานะโปรเจกต์และแนะนำขั้นตอนถัดไปเพียงขั้นตอนเดียว",
    "when": "ยังไม่แน่ใจว่าควรเริ่มตรงไหน",
    "prompt": "อ่านสถานะโปรเจกต์นี้ แล้วแนะนำ workflow ขั้นตอนถัดไปพร้อมเหตุผล"
  },
  {
    "name": "grill-workflow",
    "category": "Core workflow",
    "title": "Make the decisions first",
    "description": "ถามให้ชัดเรื่องปัญหา ขอบเขต กฎธุรกิจ และข้อจำกัด ก่อนเขียน spec",
    "when": "มีไอเดีย แต่ยังมีการตัดสินใจที่ค้างอยู่",
    "prompt": "ช่วยตั้งคำถามเพื่อกำหนดขอบเขตระบบจองห้องประชุมสำหรับทีมเล็ก"
  },
  {
    "name": "grill-design",
    "category": "Core workflow",
    "title": "Agree on the visual direction",
    "description": "บันทึกทิศทาง UI ที่ตกลงร่วมกัน เพื่อให้ขั้นตอนออกแบบใช้ข้อมูลชุดเดียวกัน",
    "when": "ต้องการกำหนด visual direction แบบเฉพาะ",
    "prompt": "ช่วยกำหนด UI design requirements สำหรับระบบจองห้องประชุมนี้"
  },
  {
    "name": "setup-project",
    "category": "Core workflow",
    "title": "Give your project a memory",
    "description": "จัดทำบริบทโปรเจกต์ เอกสารนำทาง และนโยบายการตรวจสอบงาน",
    "when": "ตัดสินใจเรื่องโปรดักต์แล้ว แต่ยังไม่มีบริบทถาวร",
    "prompt": "จัดเตรียม context และ workflow ของโปรเจกต์จากข้อสรุปที่ตกลงกัน"
  },
  {
    "name": "write-spec",
    "category": "Core workflow",
    "title": "Turn decisions into behavior",
    "description": "เขียน behavioral specification ที่มีขอบเขตและ acceptance criteria ชัดเจน",
    "when": "requirements พร้อมสำหรับการระบุพฤติกรรม",
    "prompt": "เขียน spec ของการจองห้องประชุมจาก requirements ที่ตกลงแล้ว"
  },
  {
    "name": "to-tasks",
    "category": "Core workflow",
    "title": "Make the work executable",
    "description": "แยก spec ที่พร้อมแล้วเป็นงานย่อยที่ตรวจสอบได้ พร้อมลำดับ dependency",
    "when": "มี spec ที่พร้อมนำไปพัฒนา",
    "prompt": "แยก spec ที่พร้อมแล้วเป็น implementation tasks ตาม dependency"
  },
  {
    "name": "implement-task",
    "category": "Core workflow",
    "title": "Build one focused task",
    "description": "ทำงานหนึ่ง task ให้ครบขอบเขต พร้อมหลักฐานตรวจสอบตามนโยบายโปรเจกต์",
    "when": "มี task ที่พร้อมพัฒนา",
    "prompt": "ทำ task ที่พร้อมตัวถัดไปตาม spec และบันทึก verification evidence"
  },
  {
    "name": "auto-implement",
    "category": "Core workflow",
    "title": "Move a ready batch forward",
    "description": "ตรวจ blockers ทั้งชุดก่อน แล้วทำ task ตาม dependency ทีละงาน",
    "when": "มี task หลายรายการและต้องการอนุญาตให้ทำเป็นชุด",
    "prompt": "ตรวจ prerequisites ของ tasks ใน spec นี้ แล้วทำงานที่ได้รับอนุญาตตามลำดับ"
  },
  {
    "name": "code-review",
    "category": "Core workflow",
    "title": "Close with evidence",
    "description": "ตรวจ implementation เทียบกับ spec และ acceptance criteria ก่อนตัดสินว่า done",
    "when": "implementation พร้อมรับการ review",
    "prompt": "ตรวจ task ที่อยู่ในสถานะ in_review เทียบกับ spec และหลักฐานทดสอบ"
  },
  {
    "name": "change-scope",
    "category": "Core workflow",
    "title": "Keep changed agreements consistent",
    "description": "ปรับ requirement, spec และ task ตามขอบเขตใหม่ โดยรักษางานและหลักฐานเดิมที่ยังใช้ได้",
    "when": "เปลี่ยนพฤติกรรมที่ตกลงไว้หลังวางแผนหรือเริ่มพัฒนา",
    "prompt": "เปลี่ยนเงื่อนไขยกเลิกการจองเป็นก่อนเริ่ม 6 ชั่วโมง แล้วปรับ spec และ tasks ให้ตรงกันโดยยังไม่แก้โค้ด"
  },
  {
    "name": "code-to-context",
    "category": "Brownfield",
    "title": "Understand what already exists",
    "description": "สร้างบริบทจากโค้ดพร้อมแหล่งอ้างอิง โดยรักษา context ที่เขียนไว้แล้ว",
    "when": "ต้อง onboarding หรือเติมช่องว่างข้อมูล repository ที่สำคัญ",
    "prompt": "อ่าน repository และปรับปรุง generated Codebase Context พร้อมหลักฐาน"
  },
  {
    "name": "compact-context",
    "category": "Utilities",
    "title": "Keep the handoff precise",
    "description": "ย่อ handoff ชั่วคราวโดยรักษาข้อสรุป ข้อจำกัด และคำถามที่ยังเปิดอยู่",
    "when": "handoff ยาวหรือซ้ำซ้อน",
    "prompt": "ย่อ handoff นี้โดยคง decisions, constraints และ unresolved questions"
  },
  {
    "name": "ui-design",
    "category": "Utilities",
    "title": "Design with intention",
    "description": "ช่วยจัดองค์ประกอบ UI ภายในงาน prototype หรือ implementation ที่อนุญาต",
    "when": "งาน UI ต้องการการตัดสินใจด้านดีไซน์",
    "prompt": "ปรับ UI ของ task นี้ตาม UI Design Requirements ที่ตกลงไว้"
  },
  {
    "name": "debug-task",
    "category": "Utilities",
    "title": "Find the cause before the fix",
    "description": "ทำ reproduction และทดสอบสมมติฐานเพื่อหาสาเหตุ โดยส่งหลักฐานกลับไปให้งาน implementation",
    "when": "พบ bug หรือ regression ที่ยังไม่ทราบสาเหตุ",
    "prompt": "วิเคราะห์อาการจองห้องซ้ำ พร้อม reproduction และหลักฐานสาเหตุ"
  },
  {
    "name": "to-prototype",
    "category": "Prototype",
    "title": "See it before you build it",
    "description": "สร้าง prototype ด้วย HTML, CSS และ JavaScript เพื่อช่วยตัดสินใจเรื่อง UI",
    "when": "ต้องการทดสอบโครงหน้าและ flow ก่อนสรุป spec",
    "prompt": "สร้าง prototype สำหรับ flow จองห้องตาม requirements ที่ตกลงไว้"
  },
  {
    "name": "edit-prototype",
    "category": "Prototype",
    "title": "Refine the interaction",
    "description": "ปรับเฉพาะส่วนของ prototype ตาม revision ที่ระบุ",
    "when": "มี prototype และต้องการแก้ไขแบบเจาะจง",
    "prompt": "ปรับ prototype revision ที่ระบุให้แสดง empty state ของรายการห้อง"
  },
  {
    "name": "spec-with-prototype",
    "category": "Prototype",
    "title": "Connect the screen to the spec",
    "description": "นำพฤติกรรมของ prototype ที่ยอมรับแล้วมาปรับให้ตรงกับ spec",
    "when": "ตรวจ prototype แล้วและพร้อมสรุปพฤติกรรม",
    "prompt": "ปรับ owning spec ให้ตรงกับ prototype ที่ยอมรับแล้วก่อนแยก tasks"
  },
  {
    "name": "unit-test",
    "category": "Verification",
    "title": "Verify the smallest behavior",
    "description": "ตรวจพฤติกรรมแยกส่วนด้วย test runner ของ repo และ expected results ที่เป็นอิสระ",
    "when": "task มี logic ที่ควรตรวจแยกส่วน",
    "prompt": "ตรวจพฤติกรรมแยกส่วนของ task นี้ด้วย runner และ policy ของโปรเจกต์"
  },
  {
    "name": "integration-test",
    "category": "Verification",
    "title": "Check the real boundaries",
    "description": "ตรวจการทำงานร่วมกันของ component และ service โดยไม่ mock จนขอบเขตจริงหายไป",
    "when": "task เปลี่ยนการเชื่อมต่อระหว่างส่วนของระบบ",
    "prompt": "ตรวจ boundary ระหว่าง service และ persistence ที่ task นี้เปลี่ยน"
  },
  {
    "name": "e2e-test",
    "category": "Verification",
    "title": "Follow the critical journey",
    "description": "ตรวจ user journey สำคัญที่อยู่ในขอบเขต task ด้วยระบบทดสอบของโปรเจกต์",
    "when": "task เปลี่ยนเส้นทางใช้งานสำคัญ",
    "prompt": "ตรวจ critical user journey ของ task นี้ตาม acceptance criteria"
  },
  {
    "name": "verify-feature",
    "category": "Assessments",
    "title": "Verify the whole feature",
    "description": "ตรวจ acceptance criteria และรอยต่อระหว่าง tasks พร้อมหลักฐาน โดยไม่เปลี่ยนสถานะงาน",
    "when": "ต้องการตรวจว่าฟีเจอร์ครบจริงตาม spec หรือยัง",
    "prompt": "ตรวจฟีเจอร์จองห้องตาม spec ทั้ง flow และสรุป acceptance criteria ที่ผ่าน ขาด หรือยังพิสูจน์ไม่ได้"
  },
  {
    "name": "release-check",
    "category": "Assessments",
    "title": "Know what is ready to release",
    "description": "ตรวจ candidate และ environment จากหลักฐาน build, configuration, migration และ rollback โดยไม่ deploy",
    "when": "เตรียมปล่อยเวอร์ชันและต้องการตรวจความพร้อม",
    "prompt": "ตรวจ release candidate นี้สำหรับ staging พร้อมระบุ blockers และสิ่งที่ยังไม่ยืนยัน โดยไม่ deploy"
  }
];
