'''
to generate topic distribution for new patient
'''
import lda
import numpy as np

components = np.load('data/components.npy')
test_patient = np.load('data/test_df.npy')[0,:]

def transform(X, max_iter=20, tol=1e-16):
        if isinstance(X, np.ndarray):
            # in case user passes a (non-sparse) array of shape (n_features,)
            # turn it into an array of shape (1, n_features)
            X = np.atleast_2d(X)
        doc_topic = np.empty((X.shape[0], 20))
        WS, DS = lda.utils.matrix_to_lists(X)
        # TODO: this loop is parallelizable
        for d in np.unique(DS):
            doc_topic[d] = _transform_single(WS[DS == d], max_iter, tol)
        return doc_topic

def _transform_single(doc, max_iter, tol):
    PZS = np.zeros((len(doc), 20))
    for iteration in range(max_iter + 1): # +1 is for initialization
        PZS_new = components[:, doc].T
        PZS_new *= (PZS.sum(axis=0) - PZS + 0.01)
        PZS_new /= PZS_new.sum(axis=1)[:, np.newaxis] # vector to single column matrix
        delta_naive = np.abs(PZS_new - PZS).sum()
        logger.debug('transform iter {}, delta {}'.format(iteration, delta_naive))
        PZS = PZS_new
        if delta_naive < tol:
            break
    theta_doc = PZS.sum(axis=0) / PZS.sum()
    assert len(theta_doc) == 20 
    assert theta_doc.shape == (20,)
    return theta_doc

print(transform(X=test_patient))
