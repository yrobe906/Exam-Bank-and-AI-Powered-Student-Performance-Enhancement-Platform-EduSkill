<template>
  <section class="py-20">
    <div class="max-w-6xl mx-auto grid md:grid-cols-3 gap-8 px-6">

      <!-- STUDENT CARD -->
      <div class="card group">
        <img src="@/assets/images/Sifu.png" class="card-img" />
        <h3 class="title">Students Marks</h3>
        <p class="desc">
          Students can view marks, track performance, and progress.
        </p>
      </div>

      <!-- TEACHER CARD -->
      <div class="card group">
        <img src="@/assets/images/teacher.png" class="card-img" />
        <h3 class="title">Teachers & Admin</h3>
        <p class="desc">
          Teachers update marks, notify classes and upload materials.
        </p>
      </div>

      <!-- EXAM BANK CARD -->
      <div class="card group">
        <img src="@/assets/images/exambank.png" class="card-img" />
        <h3 class="title">Exam Bank</h3>
        <p class="desc">
          Free & premium exam materials for grades and subjects.
        </p>
      </div>

    </div>
  </section>
</template>

<style scoped>
.card {
  padding: 40px;
  border-radius: 25px;
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255,255,255,0.18);
  text-align: center;
  cursor: pointer;
  transform: perspective(800px) translateZ(0);
  transition: .45s ease;
  position: relative;
  overflow: hidden;
}

/* Water drop shine */
.card::after {
  content: "";
  position: absolute;
  top: -60%;
  left: -40%;
  width: 250%;
  height: 250%;
  background: radial-gradient(circle, rgba(255,255,255,0.4), transparent 60%);
  opacity: 0;
  transition: .5s;
}

.card:hover::after {
  opacity: 0.4;
  transform: scale(1.2);
}

/* Hover animation like rising water */
.card:hover {
  transform: perspective(800px) translateY(-12px) translateZ(40px) scale(1.08);
  background: rgba(255,255,255,0.15);
  box-shadow: 0 20px 50px rgba(0,0,0,.35);
}

/* full clean images */
.card-img {
  width: 90px;
  height: 90px;
  object-fit: contain;
  margin: 0 auto 18px;
  transition: .5s;
  filter: drop-shadow(0 6px 12px rgba(0,0,0,0.25));
}

/* image hover bounce */
.card:hover .card-img {
  transform: translateY(-10px) scale(1.15);
  filter: drop-shadow(0 12px 22px rgba(0,0,0,0.4));
}

/* Titles / desc */
.title {
  font-size: 1.7rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.desc {
  color: #ddd;
  font-size: 1rem;
}
</style>
