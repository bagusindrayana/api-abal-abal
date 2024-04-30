import google.generativeai as genai
from dotenv import load_dotenv
import os
from typing import AsyncGenerator
from pydantic import BaseModel
load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

daftarPustaka = {
    "apa-style":"""
\documentclass{article}

\begin{document}

\section*{Daftar Pustaka}

\begin{enumerate}
    \item Nama Penulis. (Tahun). Judul Artikel. Judul Jurnal, Volume (Issue), Halaman-Halaman. Contoh: Lee, S. (2020). Pengaruh Kualitas Produk terhadap Kepuasan Pelanggan. Jurnal Manajemen, 10 (2), 45-60.
    \item Nama Penulis. (Tahun). Judul Buku. Penerbit. Contoh: Smith, J. (2019). The Art of Coding. Tech Publishing.
\end{enumerate}

\end{document}
""",
    "asa-style":"""
\documentclass{article}

\begin{document}

\section*{Daftar Pustaka}

\begin{enumerate}
    \item Nama Penulis. (Tahun). Judul Artikel. Judul Jurnal, Volume (Nomor), Halaman-halaman. Contoh: Becker, Howard S. 1996. “What’s Fairness Got to Do with It?” American Educational Research Journal, 33 (3), 443-461.
    \item Nama Penulis. (Tahun). Judul Buku. Kota Penerbit: Penerbit. Contoh: Giddens, Anthony. 1991. Modernity and Self-Identity. Stanford, CA: Stanford University Press.
    \item Nama Penulis Bab. (Tahun). “Judul Bab.” Dalam Nama Editor (Ed.), Judul Buku (Halaman-halaman). Kota Penerbit: Penerbit. Contoh: McLeod, Jane D. 1995. “Rape Myths in Motion Pictures.” Dalam Gender, Race and Class in Media, ed. Gail Dines dan Jean M. Humez, 289-301. Thousand Oaks, CA: Sage Publications.
    \item Nama Penulis. (Tahun). “Judul Artikel.” Nama Publikasi, Tanggal, Halaman. Contoh: Kaminer, Wendy. 1991. “The Abortion Battle: Looking Back, Moving On.” The Nation, 9 Desember, 751-755.
\end{enumerate}

\end{document}
""",
"vancouver-style":"""
\documentclass{article}

\begin{document}

\section*{Daftar Pustaka}

\begin{enumerate}
    \item Prabowo GJ dan Priyanto E. New drugs for acute respiratory distress syndrome due to avian virus. N Ind J Med. 2005;337:435-9.
    \item Grinspoon L, Bakalar JB. Marijuana: the forbidden fruit. JAMA. 1995;273(23):1875-6.
    \item Basu S, Irawan. Manajemen pemasaran modern. Yogyakarta: Liberty; 2008.
    \item Keller KL. Building customer-based brand equity: A blueprint for creating strong brands. Marketing Science Institute Cambridge, MA; 2001.
    \item Waseso DH, Darmastuti I. Perilaku konsumen untuk mengakses suaramerdeka.com. J Stud Manaj Organ. 2013;10(2):121–31.
\end{enumerate}

\end{document}
""",
"harvard-style":"""
\documentclass{article}

\begin{document}

\section*{Daftar Pustaka}

\noindent
Nama Terakhir, Nama Pertama. (Tahun). \textit{Judul Buku}. Kota Penerbit: Penerbit.

\noindent
Contoh:

\noindent
Doe, J. (2005). \textit{Lorem Ipsum}. New York: Ipsum Publishing.

\noindent
Smith, J. (2010). \textit{Dolor Sit Amet}. Chicago: Sit Amet Press.

\end{document}
""",
"chicago-style":"""
\documentclass{article}

\begin{document}

\section*{Daftar Pustaka}

\noindent
Nama Terakhir, Nama Pertama. Tahun. \textit{Judul Buku}. Kota Penerbit: Penerbit.

\noindent
Contoh:

\noindent
Doe, John. 2005. \textit{Lorem Ipsum}. New York: Ipsum Publishing.

\noindent
Smith, Jane. 2010. \textit{Dolor Sit Amet}. Chicago: Sit Amet Press.

\end{document}
"""
}

class ResponseMessage(BaseModel):
    content: str


async def response_generator(prompt: str,style:str) -> AsyncGenerator[str, None]:
    styleKey = style.lower().replace(" ","-")
    for response in model.generate_content("""
        You will be asked to make journal, your reply should only in LaTex and use """+style+""" when making bibliography format like : 
        """+daftarPustaka[styleKey]+"""

        Example question: buat jurnal yang membahas tentang kucing
        Example reply:
        ```
        \documentclass{article}
        \\title{Observasi tingkah laku kucing terhadap kondisi sebelum gempa}
        \\author{Abal-Abal}
        \\begin{document}
        
        \maketitle

        \\raggedright 
        \section*{Abstrak}
        Salah satu bagian awal dalam struktur jurnal adalah abstrak. Bagian abstrak umumnya berbentuk ringkasan yang mencakup metode, temuan, analisis, pertanyaan-pertanyaan, dan poin-poin utama dari penelitian.
        \\newline
        \\newline
        \\textbf{Kata Kunci} : \textit{English Word}, Kata Bahasa Indonesia 
        
        \section{Pendahuluan}
        Bagian selanjutnya yaitu pendahuluan. Bagian ini memuat gambaran umum mengenai subjek yang diteliti dan latar belakang masalah yang diteliti.

        \section{Metode}
        Hal-hal yang perlu dijelaskan pada bagian metode meliputi metode penelitian, sampel atau partisipan, dan peralatan yang digunakan dalam penelitian.

        \section{Hasil}
        Setelah penelitian dilakukan, langkah selanjutnya adalah memaparkan hasil temuan penelitian dan analisis terhadap data yang telah dikumpulkan dalam bagian pembahasan. Bagian ini juga dapat dilengkapi dengan grafik atau tabel.

        \section{Kesimpulan}
        Bagian kesimpulan melingkupi kesimpulan dari hasil penelitian, kekurangan, dan saran atau rekomendasi untuk penelitian berikutnya.

        \section{Daftar Pustaka}
        Pastikan untuk selalu mencantumkan sumber-sumber referensi yang digunakan dalam jurnal pada bagian daftar pustaka.

        \end{document}
        ```
                                           

        Question: buat jurnal yang membahas """+prompt+""", jelaskan dengan detail dan lengkap mulai dari bagian Abstrak hingga Kesimpulan dan Daftar Pustaka, buat dengan mengikuti format """+style+""" seperti : """+daftarPustaka[styleKey]+""", pastikan nama penulis selalu "Abal-Abal", jangan gunakan package dan thebibliography
        Reply:
        """,stream=True):
        for chunk in response:
            if hasattr(chunk, 'text'):
                yield chunk.text
            else:
                print(f'Chunk {chunk} does not have a text attribute.')
    
    yield "\n :FINISH: \n"
